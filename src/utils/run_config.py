"""Shared run settings for every LLM arm, from config/run_config.json.

B2, B3, and the pipeline all build their client from ``LLMSettings``, so they
cannot drift apart. ``check_environment`` refuses to run when CLAUDE_MODEL (the
only override the client used to honor) disagrees with the config, and
``require_same`` refuses to compare runs whose recorded settings differ.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

ROOT = Path(__file__).resolve().parents[2]
RUN_CONFIG_PATH = ROOT / "config" / "run_config.json"


class ConfigMismatch(RuntimeError):
    """Settings differ between arms, runs, or the environment. Nothing is run or compared."""


class LLMSettings(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    model: str
    effort: Literal["low", "medium", "high", "xhigh", "max"]
    max_tokens: int = Field(ge=1)
    max_attempts: int = Field(ge=1)


class Pricing(BaseModel):
    model_config = ConfigDict(extra="allow")

    model: str
    input: float
    output: float
    cache_read: float
    cache_write: float
    batch_discount: float = 0.5

    def cost(self, calls: list[dict]) -> float:
        """Estimated USD for logged calls; a call without token counts adds nothing."""
        total = 0.0
        for c in calls:
            usd = ((c.get("input_tokens") or 0) * self.input + (c.get("output_tokens") or 0) * self.output
                   + (c.get("cache_read_input_tokens") or 0) * self.cache_read
                   + (c.get("cache_creation_input_tokens") or 0) * self.cache_write) / 1e6
            total += usd * (self.batch_discount if c.get("batch") else 1.0)
        return total


class RunConfig(BaseModel):
    model_config = ConfigDict(extra="allow")

    llm: LLMSettings
    refusal_fallback: bool = False
    prompt_caching: bool = True
    batch_single_prompt_arms: bool = True
    runs: dict
    pricing_usd_per_mtok: Pricing


def load_run_config(path: Path = RUN_CONFIG_PATH) -> RunConfig:
    cfg = RunConfig.model_validate_json(Path(path).read_text())
    if cfg.refusal_fallback:
        raise ConfigMismatch("refusal_fallback is not supported: a refusal must fail the case, not switch models")
    return cfg


def check_environment(settings: LLMSettings) -> None:
    env = os.environ.get("CLAUDE_MODEL")
    if env and env != settings.model:
        raise ConfigMismatch(f"CLAUDE_MODEL={env} overrides config model {settings.model}; unset it or change "
                             "config/run_config.json so every arm uses the same model")


def require_same(settings_by_arm: dict[str, dict]) -> None:
    """Raise unless every arm recorded identical LLM settings."""
    distinct = {json.dumps(s, sort_keys=True) for s in settings_by_arm.values()}
    if len(distinct) > 1:
        detail = "; ".join(f"{arm}: {s}" for arm, s in sorted(settings_by_arm.items()))
        raise ConfigMismatch(f"LLM arms were run with different settings: {detail}")
