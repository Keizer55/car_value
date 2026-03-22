# Car Value (Used Car Price Prediction)
> *End-to-end pipeline to predict used car prices in Spain, from raw listings to a Streamlit app.*

[![Live App](https://img.shields.io/badge/Live%20App-car--value.zikzero.com-brightgreen?style=for-the-badge)](https://car-value.zikzero.com/)
**Website:** https://www.car-value.zikzero.com/
[![Python](https://img.shields.io/badge/Python-3.13-blue?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-Reference-blue?style=flat-square)](./LICENSE)

---

![Car Value Demo](./app/streamlit/assets/example.gif)

---

## Why I Built This

I was shopping for a car in 2024 and kept asking the same questions:

- Do cars depreciate heavily after the first year?
- Do premium brands retain value better?
- Are second-hand cars always a better deal?

As a data scientist, I wanted to quantify the Spanish market. This project was trained on 2024 listings, a period affected by new-car shortages and supply chain issues. Prices may have shifted since, so the model should be retrained periodically.

**Dataset size:** 15,000+ listings across 40 popular models.

**Last model trained:** February 2026 (see `models/2026-02-03/auto_ml_sklearn.pkl`).

---

## Project Overview

Pipeline flow:

1) **Process data** from raw listings into `data/processed/` (pickled DataFrame)
2) **Train** a model (notebooks / AutoML) and save artifacts to `models/<date>/`
3) **Predict** via `src/inference/predict.py`
4) **Serve UI** with Streamlit (`app/streamlit/app.py`), separating frontend from backend (`src/`)

---

## Project Structure

- `src/` — core business logic used by notebooks, scripts, and the app.
    - `scraping/`: scraping scripts (git-ignored, not included).
    - `features/`: dataset building and preprocessing.
    - `inference/`: model loading and prediction helpers.
- `app/` — frontend/presentation layer.
    - `streamlit/`: the Streamlit dashboard.
- `data/` — storage (training dataset not included).
- `models/<date>/` — versioned model artifacts.
- `notebooks/` — training and exploration notebooks.
- `config/` — scraping configuration (git-ignored, not included).

Key paths:

- `src/features/build_dataset.py` — builds `data/processed/df_auto.pkl`.
- `src/inference/predict.py` — loads a model and runs `predict(...)`.
- `app/streamlit/app.py` — Streamlit entry point.

---

## Environment

- **Run the app / inference**: `requirements-venv_app.txt` (recommended Python **3.13.x**).
- **Optional (older experiments)**: PyCaret notebooks use `requirements-venv_auto_ml_pycaret.txt` (Python **3.11.x**).

---

## Quick Start (Streamlit)

From the repo root:

```powershell
python -m venv venv_app
\.\venv_app\Scripts\Activate.ps1

python -m pip install -r requirements-venv_app.txt
streamlit run app/streamlit/app.py
```

If PowerShell execution is restricted:

```powershell
cmd /c ".\venv_app\Scripts\activate.bat"
streamlit run app/streamlit/app.py
```

Notes:
- Run `streamlit` from the repo root so imports under `src/` resolve.
- The app uses the inference helper in `src/inference/predict.py`.

---

## What’s Included

- ✅ Streamlit app under `app/streamlit/`
- ✅ Pretrained model: `models/2026-02-03/auto_ml_sklearn.pkl` (default for app)
- ✅ UI filter artifact: `data/processed/df_auto_filters.pkl`
- ❌ Full training dataset + raw HTML listings (not included)
- ❌ Scraping config under `config/` (not included)

---

## Model Artifact

Inference defaults to:
- `models/2026-02-03/auto_ml_sklearn.pkl`

See `MODEL_PATH` in `app/streamlit/utils/config.py`.

If you save a newer model, either:
- update `DEFAULT_MODEL_PATH` in `src/inference/predict.py`, or
- pass `model_path=...` when calling `predict(...)`.

---

## Optional: Rebuild Data + Retrain

If you have raw HTML locally (e.g. under `data/raw/`), rebuild the dataset:

```powershell
# Activate venv_app environment
.\venv_app\Scripts\Activate.ps1

# Build the processed dataset from raw HTML
python -m src.features.build_dataset
```

Then run the main training notebook: `notebooks/auto_ml_sklearn.ipynb`.

---

## Programmatic Inference

```python
from pathlib import Path
from src.inference.predict import predict

payload = {
    "km": 45000,                          # int value
    "fuel_type": "gasolina",              # 'diesel', 'gasolina', 'hibrido', 'hibrido ench.', 'glp', 'electrico'
    "age": 3,                             # int value
    "brand": "volkswagen",                # 'volkswagen', 'seat', 'toyota', 'renault', ...
    "segment": "C",                       # 'B', 'C', 'D', 'E', 'J', 'M'
    "body_type": "Hatchback"              # 'Hatchback', 'SUV', 'Sedan', 'MPV'
}

model_path = Path("models/2026-02-03/auto_ml_sklearn.pkl")
yhat = predict(payload, model_path=model_path)
print(yhat)
```

---

## Troubleshooting

- **Model not found**: ensure `models/2026-02-03/auto_ml_sklearn.pkl` exists (or adjust `MODEL_PATH`).
- **PowerShell activation blocked**: use `cmd /c ".\venv_app\Scripts\activate.bat"`.
- **Streamlit theme config warnings**: after upgrading Streamlit, some theme keys may become invalid. If startup logs show `is not a valid config option`, remove that key from `app/streamlit/.streamlit/config.toml` and keep only documented options.

---

## License

This project is provided as-is for educational and reference purposes.
