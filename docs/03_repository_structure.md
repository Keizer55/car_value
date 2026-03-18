# Repository Structure (Human Guide)

## Root-level map

- README.md
  - Main project introduction and quick start
- requirements-venv_app.txt
  - Dependencies for app and inference runtime
- requirements-venv_auto_ml_pycaret.txt
  - Optional dependencies for older AutoML experiments
- data/
  - Data storage (raw and processed artifacts)
- models/
  - Versioned trained model artifacts by date
- notebooks/
  - Analysis and training notebooks
- src/
  - Reusable Python modules for data preparation and inference
- app/streamlit/
  - Frontend application
- docs/
  - Human-readable documentation

## app/streamlit/

- app.py
  - Multipage entrypoint
- pages/
  - context.py: project context page
  - predictor.py: main prediction workflow
  - scope_considerations.py: assumptions and interpretation limits
- utils/
  - config.py: paths, constants, runtime switches
  - prediction_logic.py: validation and year/km scenario logic
  - data_processing.py: tabular transformations and comparison data
  - chart_renderers.py and visualizations.py: plotting and chart composition
  - ui_components.py and ui_theme.py: reusable UI and style helpers
  - analytics.py and cookie_consent.py: tracking and consent behavior
- assets/
  - Fonts and icons used by the UI
- Dockerfile
  - Container definition for deployment

## src/

- features/
  - build_dataset.py: transforms source data into processed dataset artifacts
- inference/
  - predict.py: model loading and prediction API used by the app

## data/

- data/processed/
  - Persisted artifacts used at runtime (for example filter options)
- data/raw/
  - Source data snapshots and related files

## models/

- models/<date>/auto_ml_sklearn.pkl
  - Versioned sklearn model artifacts
  - App currently points to the configured latest model in config.py

## Note about excluded topic
This structure guide intentionally does not document scraping implementation details.
