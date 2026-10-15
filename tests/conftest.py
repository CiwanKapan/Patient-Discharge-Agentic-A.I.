import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


@pytest.fixture(scope="session")
def taxonomy():
    return json.loads((ROOT / "config" / "taxonomy.json").read_text())
