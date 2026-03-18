# How It Works (End-to-End)

## High-level flow
The project follows a simple pipeline:

1. Process source data into reusable artifacts in data/processed/
2. Train and export a model artifact to models/<date>/
3. Load that model for runtime inference
4. Serve predictions and visuals in the Streamlit app

## Runtime request flow in the app
When a user interacts with the Predictor page:

1. The app loads filter options from data/processed/df_auto_filters.pkl
2. The user selects input values in the sidebar
3. Input validation checks required fields
4. The app generates multiple payloads across a year range
5. The model predicts values for each payload
6. Results are transformed into:
   - value table
   - depreciation KPIs
   - trend charts
   - brand comparison table

## Core modules involved

- app/streamlit/app.py
  - Initializes page metadata and shared UI styles
  - Configures multipage navigation
- app/streamlit/pages/predictor.py
  - Orchestrates user input, validation, predictions, and rendering
- src/inference/predict.py
  - Loads the serialized sklearn model
  - Enforces expected feature columns
  - Runs model.predict(...)
- app/streamlit/utils/*
  - Data preparation, chart rendering, and UI components

## Inference contract
The model expects these feature columns in this order:

- km
- fuel_type
- age
- brand
- segment
- body_type

Any prediction payload should map to that schema.

## Model loading behavior
The inference layer caches the loaded model in memory and reloads only if the model path changes. This improves performance and avoids repeated disk reads.

## Caching in the Streamlit layer
The app uses Streamlit cache decorators to speed up repeated interactions:

- @st.cache_resource for model and filter artifacts
- @st.cache_data for stable prediction requests

This keeps UX responsive while preserving deterministic behavior for identical inputs.
