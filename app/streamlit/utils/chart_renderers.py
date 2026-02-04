"""Chart rendering functions for the prediction results."""

import random
import streamlit as st
from typing import Dict, Any, List
import pandas as pd

from utils.visualizations import (
    create_vehicle_value_chart,
    create_fuel_type_comparison_chart,
    create_brand_comparison_chart,
    create_yearly_depreciation_chart,
    create_accumulated_depreciation_chart,
    create_dual_axis_chart,
    build_comparison_data,
)


def render_value_over_time_charts(
    df_out: pd.DataFrame,
    opts: Dict[str, Any],
    filters: Dict[str, Any],
    avg_per_year: int,
    explicit_kms: List[int],
    cached_predict,
    model_path: str
):
    """Render all 'Predicted Value Over Time' charts in tabs."""
    st.subheader("Predicted Value Over Time")
    st.write("Explore how your vehicle's estimated market value changes as it ages. Compare your vehicle with different fuel types and brands to understand depreciation patterns.")
    
    tab1, tab2, tab3 = st.tabs(["Vehicle", "By fuel type", "By brand"])
    
    with tab1:
        fig = create_vehicle_value_chart(df_out)
        st.pyplot(fig, width='stretch')
    
    with tab2:
        _render_fuel_comparison_tab(df_out, opts, filters, avg_per_year, explicit_kms, cached_predict, model_path)
    
    with tab3:
        _render_brand_comparison_tab(df_out, opts, filters, avg_per_year, explicit_kms, cached_predict, model_path)


def _render_fuel_comparison_tab(
    df_out: pd.DataFrame,
    opts: Dict[str, Any],
    filters: Dict[str, Any],
    avg_per_year: int,
    explicit_kms: List[int],
    cached_predict,
    model_path: str
):
    """Render fuel type comparison chart."""
    fuel_types = opts.get("fuel_type", [])
    if not fuel_types:
        st.info("No fuel type data available")
    else:
        base_payload = {
            "fuel_type": filters["fuel_type"],
            "brand": filters["brand"],
            "segment": filters["segment"],
            "body_type": filters["body_type"],
        }
        df_fuel = build_comparison_data(
            years=df_out["year"].tolist(),
            comparison_values=fuel_types,
            comparison_key="fuel_type",
            base_payload=base_payload,
            avg_km_per_year=avg_per_year,
            predict_func=cached_predict,
            model_path=model_path,
            explicit_kms=explicit_kms,
        )
        fig = create_fuel_type_comparison_chart(df_fuel)
        st.pyplot(fig, width='stretch')


def _render_brand_comparison_tab(
    df_out: pd.DataFrame,
    opts: Dict[str, Any],
    filters: Dict[str, Any],
    avg_per_year: int,
    explicit_kms: List[int],
    cached_predict,
    model_path: str
):
    """Render brand comparison chart."""
    brands = opts.get("brand", [])
    if not brands:
        st.info("No brand data available")
    else:
        candidates = [b for b in brands if b != filters["brand"]]
        n = min(5, len(candidates))
        sampled = random.sample(candidates, n) if n > 0 else []
        plot_brands = [filters["brand"]] + sampled if filters["brand"] else sampled[:5]
        
        base_payload = {
            "fuel_type": filters["fuel_type"],
            "brand": filters["brand"],
            "segment": filters["segment"],
            "body_type": filters["body_type"],
        }
        df_brand = build_comparison_data(
            years=df_out["year"].tolist(),
            comparison_values=plot_brands,
            comparison_key="brand",
            base_payload=base_payload,
            avg_km_per_year=avg_per_year,
            predict_func=cached_predict,
            model_path=model_path,
            explicit_kms=explicit_kms,
        )
        fig = create_brand_comparison_chart(df_brand)
        st.pyplot(fig, width='stretch')


def render_depreciation_charts(df_out: pd.DataFrame):
    """Render all depreciation analysis charts in tabs."""
    st.subheader("Depreciation Analysis")
    st.write("Analyze how your vehicle's value decreases over time. The yearly view shows the absolute value loss per year, while the accumulated view shows the total percentage decrease from the initial value.")
    
    tab_acc, tab_bar, tab_dual = st.tabs(["Accumulated", "Yearly", "Combined view"])
    
    with tab_acc:
        fig = create_accumulated_depreciation_chart(df_out)
        st.pyplot(fig, width='stretch')
    
    with tab_bar:
        fig = create_yearly_depreciation_chart(df_out)
        st.pyplot(fig, width='stretch')
    
    with tab_dual:
        fig = create_dual_axis_chart(df_out)
        st.pyplot(fig, width='stretch')
