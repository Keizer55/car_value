# Streamlit App Guide

## Purpose
The Streamlit app is the user interface for vehicle value estimation and exploration.

It lets users:

- configure vehicle characteristics
- estimate value over time
- inspect depreciation metrics
- compare selected brand vs alternatives
- read project context and scope notes

## Pages

- Predictor
  - Main interactive page to run estimations
- Project Context
  - Background and motivation
- Scope and Considerations
  - Methodological limitations and interpretation guidance

## Predictor workflow

1. Choose values in the sidebar
2. Click the predict button
3. Review:
   - projected value table
   - trend and depreciation charts
   - vehicle review KPIs
   - brand comparison table

## Inputs required for prediction

- fuel type
- brand
- segment
- body type
- current age
- current kilometers
- optional expected annual kilometers

## Validation behavior
The app blocks predictions if required fields are missing and reports clear UI errors before calling the model.

## Model and data artifacts used by the app

- Model artifact:
  - models/2026-02-03/auto_ml_sklearn.pkl
- Filter options artifact:
  - data/processed/df_auto_filters.pkl

Both paths are configured in app/streamlit/utils/config.py.

## Analytics and consent
The app can inject Microsoft Clarity if configured and accepted by the user.

- ENABLE_ANALYTICS toggles tracking
- ENABLE_COOKIE_CONSENT controls consent dialog behavior
- CLARITY_PROJECT_ID can be set via secrets or environment variable

## UX and performance notes

- Model and filter data are cached
- Prediction requests are cached by payload hash
- Multipage navigation is configured in app.py
