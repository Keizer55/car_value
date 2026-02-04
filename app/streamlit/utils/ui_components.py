"""UI component builders for the Streamlit app."""

import streamlit as st
from typing import Dict, Any, Tuple
from utils.ui_theme import sidebar_heading


def render_sidebar_filters(opts: Dict[str, Any], modify_display_name, create_display_mapping) -> Dict[str, Any]:
    """Render all sidebar filter inputs and return selected values.
    
    Args:
        opts: Dictionary containing filter options
        modify_display_name: Function to modify display names
        create_display_mapping: Function to create display mappings
        
    Returns:
        Dictionary with all selected filter values
    """
    # Render a consistent sidebar heading using the theme helper
    sidebar_heading("Filters 🚗🚙🚕🚓🏎️🚐")
    
    # Fuel type selector
    fuel_list = opts.get("fuel_type", [])
    fuel_options_display, _display_to_original_fuel = create_display_mapping(fuel_list, modify_display_name)
    fuel_default_display = fuel_options_display[0] if fuel_options_display else None
    gasolina_idx = next((i+1 for i, orig in enumerate(fuel_list) if orig.lower() == "gasolina"), 1 if fuel_default_display else 0)
    fuel_type_sel_display = st.sidebar.selectbox("Fuel type", options=["" ] + fuel_options_display, index=gasolina_idx)
    fuel_type_sel = _display_to_original_fuel.get(fuel_type_sel_display, "")

    # Brand selector
    brands_list = opts.get("brand", [])
    brand_options_display, _display_to_original = create_display_mapping(brands_list, modify_display_name)
    brand_default_display = brand_options_display[0] if brand_options_display else None
    seat_idx = next((i+1 for i, orig in enumerate(brands_list) if orig.lower() == "seat"), 1 if brand_default_display else 0)
    brand_sel_display = st.sidebar.selectbox("Brand", options=["" ] + brand_options_display, index=seat_idx)
    brand_sel = _display_to_original.get(brand_sel_display, "")

    # Segment selector
    segment_options = opts.get("segment", [])
    segment_default = segment_options[0] if segment_options else None
    segment_sel = st.sidebar.selectbox("Segment", options=[""] + segment_options, index=0 if segment_default is None else 1)

    # Body type selector
    body_options = opts.get("body_type", [])
    body_default = body_options[0] if body_options else None
    body_sel = st.sidebar.selectbox("Body type", options=[""] + body_options, index=0 if body_default is None else 1)

    # Age selector
    age_min = opts.get("age", {}).get("min", 0) or 0
    age_max = opts.get("age", {}).get("max", 0) or 0
    if age_min > age_max:
        age_min, age_max = 0, 0
    
    from utils.config import DEFAULT_AGE_VALUE
    age_default = DEFAULT_AGE_VALUE
    age_manual = st.sidebar.checkbox("Manual Age input", value=False)
    if age_manual:
        age_sel = st.sidebar.number_input("Age value", min_value=int(age_min), max_value=int(age_max), value=age_default, step=1)
    else:
        age_sel = st.sidebar.slider("Age", min_value=int(age_min), max_value=int(age_max), value=age_default)

    # KM selector
    km_manual = st.sidebar.checkbox("Manual km input", value=False)
    if km_manual:
        km_val = st.sidebar.number_input("km value", min_value=0, max_value=150000, value=20000, step=1)
    else:
        km_val = st.sidebar.slider("km", min_value=0, max_value=150000, value=20000, step=1000)

    # Expected Annual KM input
    exp_km_manual = st.sidebar.checkbox("(Optional) Annual km Increase", value=False)
    if exp_km_manual:
        expected_annual_km = st.sidebar.slider("Expected Annual KM", min_value=0, max_value=30000, value=10000, step=1000)
    else:
        expected_annual_km = None

    return {
        "fuel_type": fuel_type_sel,
        "brand": brand_sel,
        "segment": segment_sel,
        "body_type": body_sel,
        "age": age_sel,
        "km": km_val,
        "expected_annual_km": expected_annual_km,
    }


def display_selected_filters(filters: Dict[str, Any]):
    """Display a compact summary of selected filters."""
    st.info(
        f"KM: {filters['km']:,.0f}".replace(",", ".") +
        f" — Fuel: {filters['fuel_type']} — Age: {filters['age']} — "
        f"Brand: {filters['brand']} — Segment: {filters['segment']} — Body: {filters['body_type']}"
    )


def create_predict_button() -> Tuple[bool, Any]:
    """Create the predict button and return click state and success placeholder."""
    col1, col2 = st.columns([1, 6])
    with col1:
        predict_clicked = st.button("Predict")
    with col2:
        success_placeholder = st.empty()
    return predict_clicked, success_placeholder


def render_results_table(df_display, age_sel: int):
    """Render the styled results dataframe."""
    def highlight_selected_year(row):
        base_color = "#0E1117"
        highlight_color = "#232635"
        return [
            f"background-color: {highlight_color}" if row["Year"] == int(age_sel) 
            else f"background-color: {base_color}" 
            for _ in row
        ]
    
    styled_df = df_display.style.apply(highlight_selected_year, axis=1)
    st.dataframe(styled_df, width='stretch', hide_index=True)


def render_brand_comparison_table(comparison_data: list):
    """Render the brand comparison table with highlighting for selected brand.
    
    Args:
        comparison_data: List of dictionaries containing brand comparison data
    """
    import pandas as pd
    import numpy as np
    
    st.markdown("### Brand Comparison")
    st.markdown("Compare your selected brand against others with similar characteristics.")
    
    # Create dataframe
    comparison_df = pd.DataFrame(comparison_data)
    
    # Extract numeric values for gradient calculation
    devaluation_values = comparison_df["Annual Avg. Depreciation (%)"].str.replace("%", "").astype(float)
    min_val = devaluation_values.min()
    max_val = devaluation_values.max()
    
    # Apply styling to highlight the selected brand (first row) and gradient to devaluation column
    def highlight_selected_brand(row):
        base_color = "#0E1117"
        highlight_color = "#232635"
        # Highlight first row (selected brand)
        if row.name == 0:
            return [f"background-color: {highlight_color}" for _ in row]
        else:
            return [f"background-color: {base_color}" for _ in row]
    
    def color_devaluation(val):
        """Apply color gradient where higher devaluation is worse (red) and lower is better (green)."""
        try:
            numeric_val = float(val.replace("%", ""))
            if max_val == min_val:
                # All values are the same
                return "background-color: #0E1117"
            
            # Normalize to 0-1 range
            normalized = (numeric_val - min_val) / (max_val - min_val)
            
            # Color gradient: green (good/low) to red (bad/high)
            # Green: rgb(0, 200, 0), Red: rgb(200, 0, 0)
            red = int(200 * normalized)
            green = int(200 * (1 - normalized))
            
            return f"background-color: rgba({red}, {green}, 0, 0.3)"
        except:
            return "background-color: #0E1117"
    
    styled_comparison_df = comparison_df.style.apply(highlight_selected_brand, axis=1)
    styled_comparison_df = styled_comparison_df.applymap(
        color_devaluation, 
        subset=["Annual Avg. Depreciation (%)"]
    )
    
    st.dataframe(styled_comparison_df, width="stretch", hide_index=True)
