# Run and Maintenance Guide

## Local run (recommended)
From repository root:

```powershell
python -m venv venv_app
.\venv_app\Scripts\Activate.ps1
python -m pip install -r requirements-venv_app.txt
streamlit run app/streamlit/app.py
```

If PowerShell execution policy blocks activation:

```powershell
cmd /c ".\venv_app\Scripts\activate.bat"
streamlit run app/streamlit/app.py
```

## Docker run
From repository root:

```bash
docker build -t car-value-app -f app/streamlit/Dockerfile .
docker run -p 8501:8501 car-value-app
```

Open http://localhost:8501

## Changing model version
If a new model is trained and saved under models/<new-date>/:

1. Update MODEL_PATH in app/streamlit/utils/config.py
2. Restart Streamlit app
3. Validate sample predictions in Predictor page

## Key files to check during maintenance

- app/streamlit/utils/config.py
  - model path and feature/runtime toggles
- src/inference/predict.py
  - inference schema and model loading
- app/streamlit/pages/predictor.py
  - end-to-end UI orchestration

## Common operational checks

- Verify model artifact exists at configured path
- Verify data/processed/df_auto_filters.pkl exists
- Confirm dependency environment matches runtime requirements
- Confirm feature columns expected by inference are unchanged

## Troubleshooting quick list

- FileNotFoundError for model:
  - model path is wrong or artifact missing
- ImportError when loading model:
  - training-time dependencies missing in current environment
- Empty or failed predictions:
  - payload schema mismatch or invalid selections

## Documentation scope note
This maintenance guide intentionally excludes scraping operations and only covers app and inference lifecycle.
