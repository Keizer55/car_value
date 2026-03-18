# Car Value Project Overview

## What this project is
Car Value is a data product that estimates second-hand car values in Spain using a trained machine-learning model and a Streamlit web app.

The app is designed as a market reference tool. It helps users explore value trends and depreciation behavior, not to provide a legal or transactional appraisal.

## What it solves
When evaluating a used vehicle, people often ask:

- Is this car priced reasonably for its age and mileage?
- How fast might it lose value over time?
- How does this brand compare against others with similar characteristics?

This project answers those questions by combining:

- A trained regression model
- Curated filter options from processed data
- A user-facing UI with projections, charts, and comparison tables

## Main capabilities

- Predicts estimated vehicle value from key inputs:
  - kilometers
  - fuel type
  - age
  - brand
  - segment
  - body type
- Builds value-over-time projections
- Displays depreciation metrics in percent and euros
- Compares selected brand against alternatives under similar conditions
- Offers contextual pages to explain assumptions and limits

## Scope and limits

- Focused on second-hand market behavior in Spain
- Uses model-based estimation, not final transaction prices
- Results depend on model version and data recency

## Out of scope for this documentation
This documentation intentionally excludes data acquisition/scraping details and only covers:

- data processing outputs
- model inference
- Streamlit application behavior
- repository organization for app and model usage
