# Car Value (Used Car Price Prediction)

**🌐 Live App:** [https://car-value.zikzero.com/](https://car-value.zikzero.com/)

Motivation

I developed this project because I was looking to buy a car in 2024 and had many questions about the best "investment":

- Do cars depreciate heavily after the first year?
- Do premium brands retain value better?
- Are second-hand cars always a better deal?
...

As a data scientist I wanted to understand trends in the Spanish market. This work was carried out during 2024, a year marked by a rise in used-car prices caused by new-car shortages and semiconductor supply issues following the COVID-19 pandemic. Trends may have changed since then, so the model should be periodically re-evaluated; nonetheless, it serves as a useful reference.

I collected over 15,000 listings across the 40 most popular models in the Spanish market.

**Last model trained:** February 2026 (see `models/2026-02-03/auto_ml_sklearn.pkl`).

End-to-end project to process used-car listings, build a structured dataset, train an AutoML regression model, and serve price predictions via a Streamlit app.

This repo is organized as a pipeline:

1) **Process data** from raw listings into `data/processed/` (pickled DataFrame)
2) **Train** a model (notebooks / AutoML) and save artifacts to `models/<date>/`
3) **Predict** via `src/inference/predict.py`
4) **Serve UI** with Streamlit (`app/streamlit/app.py`), separating frontend code from backend logic (`src/`)

## Project structure

This project adheres to a clean separation of concerns:

- `src/` — Contains the core business logic, reusable across notebooks, scripts, and the app.
    - `scraping/`: Web scraping scripts (git-ignored, not included in the repository).
    - `features/`: Data cleaning and processing code.
    - `inference/`: Prediction logic and model loading.
- `app/` — Contains the frontend/presentation layer.
    - `streamlit/`: The Streamlit dashboard code.
- `data/` — Data storage (training dataset not included in the repo).
- `models/<date>/` — Serialized model artifacts (current default path in inference)
- `notebooks/` — Jupyter notebooks for exploration and training.
- `config/` — Configuration files for scraping (git-ignored, not included in the repository).

Key paths:

- `src/features/build_dataset.py` — processes data and writes `data/processed/df_auto.pkl`
- `src/inference/predict.py` — loads a persisted model and runs `model.predict(...)`
- `models/` — versioned model artifacts (current default path in inference)
- `app/streamlit/app.py` — Streamlit UI entry point (imports logic from `src`)

## Environment

- **Run the app / inference**: use `requirements-venv_app.txt` (recommended Python: **3.13.x**).
- **Optional (older experiments)**: PyCaret notebooks use `requirements-venv_auto_ml_pycaret.txt` (Python **3.11.x**).

## Quickstart: run the Streamlit app

From the repo root:

```powershell
python -m venv venv_app
\.\venv_app\Scripts\Activate.ps1

python -m pip install -r requirements-venv_app.txt
streamlit run app/streamlit/app.py
```

If PowerShell script execution is restricted:

```powershell
cmd /c ".\venv_app\Scripts\activate.bat"
streamlit run app/streamlit/app.py
```

Notes:
- Run `streamlit` from the repo root so imports under `src/` resolve.
- The app uses the inference helper in `src/inference/predict.py`.

## What’s included

- ✅ Streamlit app code under `app/streamlit/`
- ✅ Pretrained model artifact: `models/2026-02-03/auto_ml_sklearn.pkl` (used by default for the app)
- ✅ Reduced UI artifact for filter options: `data/processed/df_auto_filters.pkl`
- ❌ Full training dataset + raw scraped HTML listings (not included)
- ❌ Scraping configuration under `config/` (not included)

## Model artifact

Inference defaults to:
- `models/2026-02-03/auto_ml_sklearn.pkl`

See `MODEL_PATH` in `app/streamlit/utils/config.py`.

If you save a newer model, either:
- update `DEFAULT_MODEL_PATH` in `src/inference/predict.py`, or
- pass `model_path=...` when calling `predict(...)`.


## Optional: rebuild data + retrain

If you have the raw HTML files locally (e.g. under `data/raw/`), you can rebuild the processed dataset:

```powershell
# Activate venv_app environment
.\venv_app\Scripts\Activate.ps1

# Build the processed dataset from raw HTML
python -m src.features.build_dataset
```

Then run the main training notebook: `notebooks/auto_ml_sklearn.ipynb`.
## Programmatic inference

You can call the predictor from Python:

```python
from src.inference.predict import predict

payload = {
    # must match the feature columns expected by your trained model
}

yhat = predict(payload)
print(yhat)
```

## Troubleshooting

- **Model not found**: ensure `models/2026-02-03/auto_ml_sklearn.pkl` exists (or adjust `MODEL_PATH`).
- **PowerShell activation blocked**: use `cmd /c ".\venv_app\Scripts\activate.bat"`.

## License

This project is provided as-is for educational and reference purposes.
