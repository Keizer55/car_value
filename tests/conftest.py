"""Shared fixtures.

The standard's template runs every test in its own tmp_path; here the app must run from the repo root
(asset and model paths are relative to it), so the fixture moves there instead. The rule behind the
template still holds: the app and the inference code only read files, and no test writes any.
"""

import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
MODEL_PATH = REPO / "models" / "2026-02-03" / "auto_ml_sklearn.pkl"

# The app imports `utils` from app/streamlit/ and the tests import `src` from the repo root.
for p in (REPO, REPO / "app" / "streamlit"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))


@pytest.fixture
def repo_root(monkeypatch):
    monkeypatch.chdir(REPO)
    return REPO
