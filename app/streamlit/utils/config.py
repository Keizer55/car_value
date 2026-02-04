"""Configuration and constants for the Streamlit app."""
from pathlib import Path
import matplotlib.pyplot as plt

# Base directory and model path
BASE_DIR = Path(__file__).resolve().parents[3]
MODEL_PATH = BASE_DIR / "models" / "2026-02-03" / "auto_ml_sklearn.pkl"

# Filter-options artifact (safe, reduced dataset)
FILTERS_PATH = BASE_DIR / "data" / "processed" / "df_auto_filters.pkl"

# Matplotlib configuration
plt.rcParams["figure.figsize"] = (10, 5)
plt.rcParams["figure.dpi"] = 100

# Default values for selectors
DEFAULT_AGE_VALUE = 2
DEFAULT_KM_VALUE = 20000

# Font configuration
USE_CUSTOM_FONT = False  # Set to False to use Streamlit's default font
CUSTOM_FONT_NAME = "Play"
CUSTOM_FONT_PATHS = {
    "regular": "app/streamlit/assets/fonts/futuristic_1/Play-Regular.ttf",
    "bold": "app/streamlit/assets/fonts/futuristic_1/Play-Bold.ttf"
}
