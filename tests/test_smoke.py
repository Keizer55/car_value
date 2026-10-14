"""Smoke tests: the pickled model still loads and answers as before, and every page runs.

They exist mostly for dependency upgrades. The model and the filter options are pickles, so a new
scikit-learn or pandas can break them silently; these tests catch that before a deploy.
"""

import pytest

from conftest import MODEL_PATH

# Initial value (age 0, 0 km) of the app's default car, from the 2026-02-03 model. If the model is
# retrained, update this number together with MODEL_PATH.
REFERENCE_PAYLOAD = {
    "km": 0,
    "fuel_type": "gasolina",
    "age": 0,
    "brand": "seat",
    "segment": "B",
    "body_type": "Hatchback",
}
REFERENCE_VALUE = 20667.25


def test_model_reproduces_reference_prediction():
    from src.inference.predict import predict

    value = float(predict(REFERENCE_PAYLOAD, model_path=MODEL_PATH)[0])
    assert value == pytest.approx(REFERENCE_VALUE, abs=0.01)


def test_filter_options_load():
    import pandas as pd

    df = pd.read_pickle(MODEL_PATH.parents[2] / "data" / "processed" / "df_auto_filters.pkl")
    for col in ("fuel_type", "brand", "segment", "body_type"):
        assert df[col].notna().any(), col


@pytest.fixture
def app(repo_root):
    from streamlit.testing.v1 import AppTest

    at = AppTest.from_file(str(repo_root / "app" / "streamlit" / "app.py"), default_timeout=120)
    at.run()
    return at


@pytest.mark.parametrize(
    "page", ["pages/predictor.py", "pages/context.py", "pages/scope_considerations.py"]
)
def test_page_runs(app, page):
    app.switch_page(page)
    app.run()
    assert not app.exception, [str(e.value) for e in app.exception]


def test_predict_button_shows_results(app):
    app.switch_page("pages/predictor.py")
    app.run()
    next(b for b in app.button if b.label == "Predict").click().run()
    assert not app.exception, [str(e.value) for e in app.exception]
    assert any("Calculations processed" in s.value for s in app.success)
    assert len(app.dataframe) >= 1
