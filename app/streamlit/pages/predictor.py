import json
import sys
import os
import pandas as pd
import streamlit as st

from utils.config import BASE_DIR, MODEL_PATH, FILTERS_PATH
from utils.data_processing import (
    modify_display_name,
    load_filter_options,
    build_prediction_payloads,
    calculate_depreciation_metrics,
    format_dataframe_for_display,
    create_display_mapping,
    calculate_brand_comparison_data,
)
from utils.ui_components import (
    render_sidebar_filters,
    display_selected_filters,
    create_predict_button,
    render_results_table,
    render_brand_comparison_table,
)
from utils.prediction_logic import (
    calculate_years_and_kms,
    validate_payloads,
    validate_selections,
    validate_predictions,
)
from utils.chart_renderers import (
    render_value_over_time_charts,
    render_depreciation_charts,
)
from utils.ui_theme import footer

if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

from src.inference.predict import load_model, predict

@st.cache_resource(show_spinner=True)
def get_model():
    return load_model(MODEL_PATH)


@st.cache_resource(show_spinner=True)
def get_filter_options():
    return load_filter_options(FILTERS_PATH)


@st.cache_data
def cached_predict(payloads_json: str, model_path: str):
    """Cache wrapper around `predict` that accepts a JSON string (stable hashable).

    `payloads_json` should be produced with `json.dumps(payloads, sort_keys=True)`.
    """
    payloads = json.loads(payloads_json)
    return predict(payloads, model_path=model_path)


# Inject Open Graph meta tags for social sharing
st.markdown(
    '''
    <meta property="og:title" content="Car Value Predictor" />
    <meta property="og:description" content="Estimate your car's value with AI, using data from 15,000+ vehicles in Spain." />
    <meta property="og:image" content="https://car-value.zikzero.com/app/streamlit/assets/icons/favicon.ico" />
    <meta property="og:url" content="https://car-value.zikzero.com/" />
    ''',
    unsafe_allow_html=True
)
st.title("Car Value Predictor")
st.write("Use the sidebar selectors to configure the input variables used for prediction.")

# Load filter options and render sidebar filters
opts = get_filter_options()
filters = render_sidebar_filters(opts, modify_display_name, create_display_mapping)

# Display selected filters
display_selected_filters(filters)

# Create predict button
predict_clicked, success_placeholder = create_predict_button()

if predict_clicked:
    try:
        # Validate selections
        error_msg = validate_selections(filters)
        if error_msg:
            st.error(error_msg)
        else:
            # Calculate years and KMs
            years, explicit_kms, avg_per_year = calculate_years_and_kms(
                cur_age=int(filters["age"]),
                cur_km=int(filters["km"]),
                expected_annual_km=filters["expected_annual_km"]
            )

            # Build prediction payloads
            payloads = build_prediction_payloads(
                years=years,
                avg_km_per_year=avg_per_year,
                explicit_kms=explicit_kms,
                fuel_type=filters["fuel_type"],
                brand=filters["brand"],
                segment=filters["segment"],
                body_type=filters["body_type"],
            )

            # Validate payloads
            error_msg = validate_payloads(payloads)
            if error_msg:
                st.error(error_msg)
            else:
                # Make predictions
                preds = cached_predict(json.dumps(payloads, sort_keys=True), str(MODEL_PATH))
                df_base = pd.DataFrame({
                    "year": years,
                    "km": [p["km"] for p in payloads],
                    "prediction": preds
                })

                # Validate predictions
                error_msg = validate_predictions(preds, df_base)
                if error_msg:
                    st.error(error_msg)
                else:
                    # Process and display results
                    df_out = calculate_depreciation_metrics(df_base)
                    df_display = format_dataframe_for_display(df_out)
                    
                    success_placeholder.success("Calculations processed with the model")
                    
                    # Render results table
                    render_results_table(df_display, filters["age"])
                    
                    # Render value over time charts
                    render_value_over_time_charts(
                        df_out, opts, filters, avg_per_year, explicit_kms,
                        cached_predict, str(MODEL_PATH)
                    )
                    
                    # Render depreciation charts
                    render_depreciation_charts(df_out)

                    # --- Vehicle Review Block ---
                    st.markdown("---")
                    st.subheader("Vehicle Review")

                    # Compose paragraph with bolded selections
                    brand = f"**{filters['brand']}**"
                    segment = f"**{filters['segment']}**"
                    fuel = f"**{filters['fuel_type']}**"
                    st.markdown(
                        f"This section compares your selected vehicle ({brand}, {segment}, {fuel}) against others in the dataset. Below are key indicators for your configuration."
                    )

                    # KPIs
                    # Estimated initial value (value at year 0)
                    initial_value = df_out.loc[df_out['year'] == 0, 'value'].values[0] if 'value' in df_out.columns else df_out.loc[df_out['year'] == 0, 'prediction'].values[0]

                    # Annual average depreciation (%) and (€) from df_out, excluding year = 0, using correct columns
                    df_kpi = df_out[df_out['year'] != 0] if 'year' in df_out.columns else df_out
                    avg_drop_pct = df_kpi['depreciation_pct'].mean() if 'depreciation_pct' in df_kpi.columns else 0
                    avg_drop_eur = df_kpi['depreciation'].mean() if 'depreciation' in df_kpi.columns else 0

                    kpi1, kpi2, kpi3 = st.columns(3)
                    kpi1.metric("Estimated Initial Value (€)", f"{initial_value:,.0f}")
                    kpi2.metric("Annual Avg. Depreciation (%)", f"{avg_drop_pct:.2f}%")
                    kpi3.metric("Annual Avg. Depreciation (€)", f"{avg_drop_eur:,.0f}")

                    # --- Brand Comparison Table ---
                    all_brands = opts.get('brand', [])
                    comparison_data = calculate_brand_comparison_data(
                        all_brands=all_brands,
                        selected_brand=filters["brand"],
                        filters=filters,
                        avg_km_per_year=avg_per_year,
                        cached_predict_func=cached_predict,
                        model_path=str(MODEL_PATH)
                    )
                    render_brand_comparison_table(comparison_data)
    except Exception as exc:  # noqa: BLE001
        st.error(f"Error: {exc}")

# Display model version
model_version = os.path.basename(os.path.dirname(str(MODEL_PATH)))
footer(f"Model calculated with over 15,000 vehicles from Spain. Model Version: {model_version}.")
