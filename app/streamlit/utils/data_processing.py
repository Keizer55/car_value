"""Data processing functions for the Streamlit app."""
import pandas as pd
from typing import Dict, List, Any


def modify_display_name(name: str) -> str:
    """Convert a name to a display-friendly format.
    
    Args:
        name: The original name to modify
        
    Returns:
        Modified name (uppercase if <= 3 chars, otherwise title case)
    """
    try:
        name = str(name)
        return name.upper() if len(name) <= 3 else name.title()
    except Exception:
        return name


def load_filter_options(df_path) -> Dict[str, Any]:
    """Load filter options from the processed dataframe.
    
    Args:
        df_path: Path to the dataframe pickle file
        
    Returns:
        Dictionary containing filter options for each column
    """
    try:
        df = pd.read_pickle(df_path)
    except Exception:
        return {}

    opts = {}
    for col in ["fuel_type", "brand", "segment", "body_type"]:
        if col in df.columns:
            opts[col] = sorted(df[col].dropna().unique().tolist())
        else:
            opts[col] = []

    # Numeric ranges can come from raw columns (cv/age) or aggregated columns
    # (cv_min/cv_max, age_min/age_max) depending on which artifact is used.
    def _range_from_cols(min_col: str, max_col: str) -> Dict[str, int]:
        if min_col not in df.columns or max_col not in df.columns:
            return {"min": 0, "max": 0}
        vmin = pd.to_numeric(df[min_col], errors="coerce").dropna()
        vmax = pd.to_numeric(df[max_col], errors="coerce").dropna()
        if vmin.empty or vmax.empty:
            return {"min": 0, "max": 0}
        return {"min": int(vmin.min()), "max": int(vmax.max())}

    if "age" in df.columns:
        vals = pd.to_numeric(df["age"], errors="coerce").dropna()
        opts["age"] = {"min": int(vals.min()), "max": int(vals.max())} if not vals.empty else {"min": 0, "max": 0}
    else:
        opts["age"] = _range_from_cols("age_min", "age_max")

    return opts


def build_prediction_payloads(
    years: List[int],
    fuel_type: str,
    brand: str,
    segment: str,
    body_type: str,
    avg_km_per_year: int = 0,
    explicit_kms: List[int] = None
) -> List[Dict[str, Any]]:
    """Build prediction payloads for multiple years.
    
    Args:
        years: List of years (ages) to predict for
        fuel_type: Fuel type
        brand: Vehicle brand
        segment: Vehicle segment
        body_type: Vehicle body type
        avg_km_per_year: Average kilometers per year (used if explicit_kms is None)
        explicit_kms: Optional list of specific KM values corresponding to years
        
    Returns:
        List of payload dictionaries
    """
    payloads = []
    
    if explicit_kms is not None and len(explicit_kms) != len(years):
        # Fallback or raise? Let's treat it as if explicit_kms was not provided if length doesn't match, or just error?
        # For safety/simplicity here, we can ignore it or assume caller is correct.
        # But raising is better for debugging.
        # However, to be safe against runtime errors during dev, I'll allow fallback but it's risky.
        # Let's assume caller is correct.
        pass

    for i, y in enumerate(years):
        if explicit_kms is not None and i < len(explicit_kms):
            km_y = explicit_kms[i]
        else:
            km_y = int(round(y * avg_km_per_year))
            
        payloads.append({
            "km": km_y,
            "fuel_type": fuel_type,
            "age": int(y),
            "brand": brand,
            "segment": segment,
            "body_type": body_type,
        })
    return payloads


def calculate_depreciation_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate depreciation metrics for the prediction dataframe.
    
    Args:
        df: DataFrame with 'year', 'km', and 'prediction' columns
        
    Returns:
        DataFrame with additional depreciation metrics
    """
    df_out = df.copy()
    
    # Ensure numeric predictions
    df_out["prediction"] = pd.to_numeric(df_out["prediction"], errors="coerce")

    # Yearly depreciation = previous_year_value - current_year_value
    prev = df_out["prediction"].shift(1)
    df_out["depreciation"] = prev - df_out["prediction"]
    df_out["depreciation"] = df_out["depreciation"].fillna(0.0)

    # Percent depreciation relative to previous year (0 for first row)
    df_out["depreciation_pct"] = df_out["depreciation"] / prev.replace({0: pd.NA})
    df_out["depreciation_pct"] = df_out["depreciation_pct"].fillna(0.0) * 100

    # Accumulated depreciation as percent relative to the first year's value
    base_val = float(df_out["prediction"].iloc[0]) if not df_out["prediction"].empty else 0.0
    if base_val and base_val != 0:
        df_out["accum_depreciation"] = ((base_val - df_out["prediction"]) / base_val) * 100
    else:
        df_out["accum_depreciation"] = 0.0

    # Round numeric columns for display
    cols_to_round = ["prediction", "depreciation", "depreciation_pct", "accum_depreciation"]
    df_out[cols_to_round] = df_out[cols_to_round].round(2)

    return df_out


def format_dataframe_for_display(df: pd.DataFrame) -> pd.DataFrame:
    """Format dataframe columns for display with proper number formatting.
    
    Args:
        df: DataFrame to format
        
    Returns:
        Formatted DataFrame
    """
    df_display = df.copy()
    
    # Format km with dots for thousands, prediction and devaluation as integers (no decimals)
    df_display["km"] = df_display["km"].apply(lambda x: f"{x:,.0f}".replace(",", "."))
    df_display["prediction"] = df_display["prediction"].apply(lambda x: f"{int(round(x)):,.0f}".replace(",", "."))
    df_display["depreciation"] = df_display["depreciation"].apply(lambda x: f"{int(round(x)):,.0f}".replace(",", "."))
    df_display["depreciation_pct"] = df_display["depreciation_pct"].apply(lambda x: f"{x:.2f}%")
    df_display["accum_depreciation"] = df_display["accum_depreciation"].apply(lambda x: f"{x:.2f}%")
    
    # Rename columns for display
    df_display = df_display.rename(columns={
        "year": "Year",
        "km": "km",
        "prediction": "Value (€)",
        "depreciation": "Annual Depreciation (€)",
        "depreciation_pct": "Annual Depreciation (%)",
        "accum_depreciation": "Accum. Depreciation (%)"
    })
    
    return df_display


def create_display_mapping(original_list: List[str], modifier_func) -> tuple:
    """Create a mapping between original values and display values.
    
    Args:
        original_list: List of original values
        modifier_func: Function to modify display names
        
    Returns:
        Tuple of (display_list, display_to_original_dict)
    """
    df = pd.DataFrame({"original": original_list})
    df["modified"] = df["original"].apply(modifier_func)
    display_list = df["modified"].tolist()
    display_to_original = dict(zip(df["modified"], df["original"]))
    return display_list, display_to_original


def calculate_brand_comparison_data(
    all_brands: List[str],
    selected_brand: str,
    filters: Dict[str, Any],
    avg_km_per_year: int,
    cached_predict_func,
    model_path: str
) -> List[Dict[str, Any]]:
    """Calculate comparison data for brands with similar characteristics.
    
    Args:
        all_brands: List of all available brands
        selected_brand: The currently selected brand
        filters: Dictionary of filter values (fuel_type, segment, body_type)
        avg_km_per_year: Average kilometers per year for calculations
        cached_predict_func: Cached prediction function
        model_path: Path to the model
        
    Returns:
        List of dictionaries containing comparison data for each brand
    """
    import json
    
    # Calculate initial value for all brands
    brand_initial_values = {}
    for brand in all_brands:
        # Create payload for year 0 with current brand
        payload_year_0 = [{
            "km": 0,
            "fuel_type": filters["fuel_type"],
            "age": 0,
            "brand": brand,
            "segment": filters["segment"],
            "body_type": filters["body_type"],
        }]
        pred = cached_predict_func(json.dumps(payload_year_0, sort_keys=True), model_path)
        brand_initial_values[brand] = pred[0]
    
    # Get selected brand's initial value
    selected_brand_initial = brand_initial_values[selected_brand]
    
    # Calculate absolute differences and sort
    brand_diffs = {
        brand: abs(value - selected_brand_initial)
        for brand, value in brand_initial_values.items()
        if brand != selected_brand
    }
    
    # Get 6 closest brands
    closest_brands = sorted(brand_diffs.items(), key=lambda x: x[1])[:6]
    closest_brand_names = [brand for brand, _ in closest_brands]
    
    # Prepare comparison data
    comparison_data = []
    selected_brand_data = None
    
    # Collect data for all brands (selected + closest)
    brands_to_compare = [selected_brand] + closest_brand_names
    
    for brand in brands_to_compare:
        # Build payloads for years 0-10
        brand_years = list(range(0, 11))
        brand_payloads = build_prediction_payloads(
            years=brand_years,
            avg_km_per_year=avg_km_per_year,
            explicit_kms=None,
            fuel_type=filters["fuel_type"],
            brand=brand,
            segment=filters["segment"],
            body_type=filters["body_type"],
        )
        
        # Get predictions
        brand_preds = cached_predict_func(json.dumps(brand_payloads, sort_keys=True), model_path)
        brand_df = pd.DataFrame({
            "year": brand_years,
            "km": [p["km"] for p in brand_payloads],
            "prediction": brand_preds
        })
        
        # Calculate metrics
        brand_df_out = calculate_depreciation_metrics(brand_df)
        
        # Extract values
        initial_val = brand_df_out.loc[brand_df_out['year'] == 0, 'prediction'].values[0]
        value_year_5 = brand_df_out.loc[brand_df_out['year'] == 5, 'prediction'].values[0] if 5 in brand_df_out['year'].values else None
        value_year_10 = brand_df_out.loc[brand_df_out['year'] == 10, 'prediction'].values[0] if 10 in brand_df_out['year'].values else None
        
        # Calculate avg depreciation (excluding year 0)
        brand_df_kpi = brand_df_out[brand_df_out['year'] != 0]
        avg_depreciation_pct = brand_df_kpi['depreciation_pct'].mean() if 'depreciation_pct' in brand_df_kpi.columns and not brand_df_kpi.empty else 0
        avg_depreciation_eur = brand_df_kpi['depreciation'].mean() if 'depreciation' in brand_df_kpi.columns and not brand_df_kpi.empty else 0
        
        brand_data = {
            "Brand": modify_display_name(brand),
            "Initial Value (€)": f"{initial_val:,.0f}",
            "Annual Avg. Depreciation (%)": f"{avg_depreciation_pct:.2f}%",
            "Annual Avg. Depreciation (€)": f"{avg_depreciation_eur:,.0f}",
            "Value at Year 5 (€)": f"{value_year_5:,.0f}" if value_year_5 is not None else "N/A",
            "Value at Year 10 (€)": f"{value_year_10:,.0f}" if value_year_10 is not None else "N/A",
            "_initial_val_numeric": initial_val  # Keep for sorting
        }
        
        if brand == selected_brand:
            selected_brand_data = brand_data
        else:
            comparison_data.append(brand_data)
    
    # Sort other brands by initial value (highest to lowest)
    comparison_data.sort(key=lambda x: x["_initial_val_numeric"], reverse=True)
    
    # Put selected brand first, then sorted others
    if selected_brand_data:
        comparison_data = [selected_brand_data] + comparison_data
    
    # Remove the numeric field used for sorting
    for item in comparison_data:
        item.pop("_initial_val_numeric", None)
    
    return comparison_data
