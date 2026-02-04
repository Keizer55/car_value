from pathlib import Path
from typing import Any, Dict, Iterable, Union

import pandas as pd
import joblib


BASE_DIR = Path(__file__).resolve().parents[2]

_MODEL = None
_MODEL_PATH = None


def load_model(model_path: Path ):
    """Load the persisted sklearn model (joblib).

    Expects `model_path` to point to a joblib-serialized sklearn estimator or
    full sklearn `Pipeline` (including preprocessing). Caches the model for reuse.
    """
    global _MODEL, _MODEL_PATH

    model_path = Path(model_path)
    if _MODEL is not None and _MODEL_PATH == model_path:
        return _MODEL

    if not model_path.exists():
        raise FileNotFoundError(f"Model file not found at {model_path}")

    try:
        model = joblib.load(model_path)
    except ModuleNotFoundError as exc:
        # Loading requires the same libraries that were present when the model was saved.
        raise ImportError(
            "Missing dependency while loading the sklearn model. "
            "Install the packages used during training in this environment (at minimum scikit-learn)."
        ) from exc

    _MODEL = model
    _MODEL_PATH = model_path
    return model


def _to_dataframe(payload: Union[Dict[str, Any], Iterable[Dict[str, Any]], pd.DataFrame]) -> pd.DataFrame:
    if isinstance(payload, pd.DataFrame):
        return payload
    if isinstance(payload, dict):
        return pd.DataFrame([payload])
    # Assume iterable of dicts
    return pd.DataFrame(payload)


def predict(payload: Union[Dict[str, Any], Iterable[Dict[str, Any]], pd.DataFrame], model_path: Path):
    """Run inference using the trained model.

    Args:
        payload: Either a dict (single record), an iterable of dicts, or a DataFrame
                 containing the feature columns expected by the model.
        model_path: Optional override for the model artifact path.

    Returns:
        A pandas Series or ndarray of predictions from the model.
    """
    model = load_model(model_path)
    df = _to_dataframe(payload)
    # Ensure correct column order and names
    expected_cols = ['km','fuel_type','age','brand','segment','body_type']
    df = df.reindex(columns=expected_cols)
    return model.predict(df)
