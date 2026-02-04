import streamlit as st
from utils.ui_theme import sidebar_heading, footer

st.title("Project Context")

# Render a small sidebar heading for context/about
sidebar_heading("About", "ℹ️")

st.markdown("""
## Car Value (Used Car Price Prediction)

**Motivation**

This project was developed in 2024 while searching for a car and trying to answer questions like:

- Do cars depreciate heavily after the first year?
- Do premium brands retain value better?
- Are second-hand cars always a better deal?

As a data scientist, I wanted to understand trends in the Spanish market. The project was carried out during a year marked by a rise in used-car prices due to new-car shortages and semiconductor supply issues following the COVID-19 pandemic. Trends may have changed since then, so the model should be periodically re-evaluated; nonetheless, it serves as a useful reference for the 2024 market.

Over 15,000 listings from the 40 most popular models in Spain were scraped (the raw scraping code is not included in this repository).

**Last model trained:** February 2026 (see `models/2026-02-03/auto_ml_sklearn.pkl`).

---

### How it works

1.  **Data Collection**: Listing pages were scraped to gather raw data on various vehicles.
2.  **Data Processing**: The raw data was cleaned and structured into a dataset, extracting key features like mileage, age, brand, segment, body type, and fuel type.
3.  **Model Training**: An AutoML approach was used to train regression models. The best performing model is used here to generate predictions.
4.  **Prediction**: Based on the parameters you input (Age, KM, Brand, etc.), the model estimates the current fair price.

### Features Used

The model considers the following attributes to predict the price:

*   **Brand**: The manufacturer of the car (e.g., Seat, Renault, Volkswagen).
*   **Segment**: The market segment of the car (e.g., compact, SUV).
*   **Body Type**: The physical shape of the car (e.g., sedan, hatchback).
*   **Fuel Type**: The type of fuel the car uses (e.g., Gasoline, Diesel, Hybrid).
*   **Age**: The age of the vehicle in years.
*   **KM**: The total kilometers driven.

### Goal

The goal is to provide a reliable estimate of a car's value to help buyers and sellers make informed decisions.
""")

# Small footer
footer("Data collected from 15,000+ vehicle listings · Built with ❤")
