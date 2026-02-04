"""Core prediction logic and data processing."""

import json
from typing import List, Dict, Any, Tuple, Optional
import pandas as pd


def calculate_years_and_kms(
    cur_age: int, 
    cur_km: int, 
    expected_annual_km: Optional[int]
) -> Tuple[List[int], List[int], int]:
    """Calculate years range and corresponding KMs for predictions.
    
    Args:
        cur_age: Current vehicle age
        cur_km: Current vehicle kilometers
        expected_annual_km: Optional expected annual km increase
        
    Returns:
        Tuple of (years list, explicit_kms list, avg_per_year)
    """
    avg_per_year = int(cur_km / cur_age) if cur_age > 0 else int(cur_km)
    
    if cur_age < 10:
        years = list(range(0, 11))
    else:
        years = list(range(cur_age, cur_age + 4))
    
    explicit_kms = []
    for y in years:
        if y <= cur_age:
            # For past or current age, linear accumulation to current state
            if cur_age > 0:
                explicit_kms.append(int(round(y * (cur_km / cur_age))))
            else:
                explicit_kms.append(int(round(y * avg_per_year)))
        else:
            # Future years
            if expected_annual_km is not None:
                explicit_kms.append(cur_km + (y - cur_age) * int(expected_annual_km))
            else:
                explicit_kms.append(int(round(y * avg_per_year)))
    
    return years, explicit_kms, avg_per_year


def validate_payloads(payloads: List[Dict[str, Any]]) -> Optional[str]:
    """Validate prediction payloads.
    
    Args:
        payloads: List of payload dictionaries
        
    Returns:
        Error message if validation fails, None otherwise
    """
    if not payloads:
        return "Prediction failed: No payloads generated."
    
    missing_fields = []
    for p in payloads:
        if not p.get("fuel_type"): missing_fields.append("fuel_type")
        if not p.get("brand"): missing_fields.append("brand")
        if not p.get("segment"): missing_fields.append("segment")
        if not p.get("body_type"): missing_fields.append("body_type")
    
    if missing_fields:
        unique_missing = list(set(missing_fields))
        return f"Prediction could not be made: missing fields {unique_missing}"
    
    return None


def validate_selections(filters: Dict[str, Any]) -> Optional[str]:
    """Validate that all required filters are selected.
    
    Args:
        filters: Dictionary of filter selections
        
    Returns:
        Error message if validation fails, None otherwise
    """
    if not filters["fuel_type"] or not filters["brand"] or \
       not filters["segment"] or not filters["body_type"]:
        return "Please select Fuel type, Brand, Segment and Body type in the sidebar."
    return None


def validate_predictions(preds, df_base: pd.DataFrame) -> Optional[str]:
    """Validate prediction results.
    
    Args:
        preds: Predictions from model
        df_base: Base dataframe with predictions
        
    Returns:
        Error message if validation fails, None otherwise
    """
    if preds is None or len(preds) == 0:
        return "Prediction failed: model returned no results."
    
    if df_base.empty:
        return "Prediction failed: input data is empty."
    
    return None
