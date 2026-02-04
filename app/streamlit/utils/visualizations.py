"""Visualization functions for the Streamlit app."""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from typing import List


def create_vehicle_value_chart(df: pd.DataFrame) -> plt.Figure:
    """Create a line chart showing vehicle value over time.
    
    Args:
        df: DataFrame with 'year' and 'prediction' columns
        
    Returns:
        Matplotlib figure with styled dark theme
    """
    fig, ax = plt.subplots()
    fig.patch.set_facecolor("#181B23")
    ax.set_facecolor("#181B23")
    sns.lineplot(data=df, x="year", y="prediction", marker="o", ax=ax)
    ax.set_xlabel("Year (age)", color="white")
    ax.set_ylabel("Predicted value", color="white")
    ax.set_title("Year-by-year predicted value (vehicle)", color="white")
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    if ax.get_legend() is not None:
        ax.get_legend().remove()
    # Add value labels on each point
    for idx, row in df.iterrows():
        label = f"{row['prediction']:,.0f}".replace(",", ".")
        y_offset = (df['prediction'].max() - df['prediction'].min()) * 0.03
        ax.text(row['year'], row['prediction'] + y_offset, label, ha='center', va='bottom', 
                fontsize=11, fontweight='normal', color='white')
    # Set axis spine colors to white and hide top/right
    for position, spine in ax.spines.items():
        spine.set_color('white')
        if position in ["top", "right"]:
            spine.set_visible(False)
    fig.tight_layout()
    return fig


def create_vehicle_value_chart_seaborn(df: pd.DataFrame) -> plt.Figure:
    """Create a seaborn-styled line chart showing vehicle value over time.
    
    Args:
        df: DataFrame with 'year' and 'prediction' columns
        
    Returns:
        Matplotlib figure with seaborn styling and dark theme
    """
    fig = plt.figure()
    ax = fig.add_subplot(111)
    fig.patch.set_facecolor("#181B23")
    ax.set_facecolor("#181B23")
    sns.lineplot(data=df, x="year", y="prediction", marker="o", linewidth=2.5, ax=ax)
    ax.set_xlabel("Year (age)", color="white")
    ax.set_ylabel("Predicted value", color="white")
    ax.set_title("Year-by-year predicted value (vehicle) - Seaborn style", color="white")
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    for idx, row in df.iterrows():
        label = f"{row['prediction']:,.0f}".replace(",", ".")
        y_offset = (df['prediction'].max() - df['prediction'].min()) * 0.03
        ax.text(row['year'], row['prediction'] + y_offset, label, ha='center', va='bottom', 
                fontsize=11, fontweight='normal', color='white')
    # Set axis spine colors to white and hide top/right
    for position, spine in ax.spines.items():
        spine.set_color('white')
        if position in ["top", "right"]:
            spine.set_visible(False)
    fig.tight_layout()
    return fig


def create_fuel_type_comparison_chart(df: pd.DataFrame) -> plt.Figure:
    """Create a line chart comparing predicted values across fuel types.
    
    Args:
        df: DataFrame with 'year', 'prediction', and 'fuel_type' columns
        
    Returns:
        Matplotlib figure
    """
    fig, ax = plt.subplots()
    fig.patch.set_facecolor("#181B23")
    ax.set_facecolor("#181B23")
    sns.lineplot(data=df, x="year", y="prediction", hue="fuel_type", marker="o", ax=ax)
    ax.set_xlabel("Year (age)", color="white")
    ax.set_ylabel("Predicted value", color="white")
    ax.set_title("Predicted value by fuel type", color="white")
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    legend = ax.get_legend()
    if legend is not None:
        legend.get_frame().set_facecolor('#181B23')
        legend.get_frame().set_edgecolor('white')
        legend.get_title().set_color('white')
        for text in legend.get_texts():
            text.set_color('white')
            
    # Set axis spine colors to white and hide top/right
    for position, spine in ax.spines.items():
        spine.set_color('white')
        if position in ["top", "right"]:
            spine.set_visible(False)

    fig.tight_layout()
    return fig


def create_brand_comparison_chart(df: pd.DataFrame) -> plt.Figure:
    """Create a line chart comparing predicted values across brands.
    
    Args:
        df: DataFrame with 'year', 'prediction', and 'brand' columns
        
    Returns:
        Matplotlib figure
    """
    fig, ax = plt.subplots()
    fig.patch.set_facecolor("#181B23")
    ax.set_facecolor("#181B23")
    sns.lineplot(data=df, x="year", y="prediction", hue="brand", marker="o", ax=ax)
    ax.set_xlabel("Year (age)", color="white")
    ax.set_ylabel("Predicted value", color="white")
    ax.set_title("Predicted value by brand", color="white")
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    legend = ax.get_legend()
    if legend is not None:
        legend.get_frame().set_facecolor('#181B23')
        legend.get_frame().set_edgecolor('white')
        legend.get_title().set_color('white')
        for text in legend.get_texts():
            text.set_color('white')
            
    # Set axis spine colors to white and hide top/right
    for position, spine in ax.spines.items():
        spine.set_color('white')
        if position in ["top", "right"]:
            spine.set_visible(False)

    fig.tight_layout()
    return fig


def create_yearly_depreciation_chart(df: pd.DataFrame) -> plt.Figure:
    """Create a bar chart showing yearly depreciation.
    
    Args:
        df: DataFrame with 'year' and 'depreciation' columns
        
    Returns:
        Matplotlib figure
    """
    fig, ax = plt.subplots()
    fig.patch.set_facecolor("#181B23")
    ax.set_facecolor("#181B23")
    sns.barplot(data=df, x="year", y="depreciation", color="tab:blue", ax=ax)
    ax.set_xlabel("Year (age)", color="white")
    ax.set_ylabel("Yearly depreciation", color="white")
    ax.set_title("Yearly depreciation (absolute)", color="white")
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    for container in ax.containers:
        labels = [f"{v.get_height():,.0f}".replace(",", ".") if v.get_height() != 0 else "" 
                  for v in container]
        ax.bar_label(container, labels=labels, padding=3, color='white')
    
    # Set axis spine colors to white and hide top/right
    for position, spine in ax.spines.items():
        spine.set_color('white')
        if position in ["top", "right"]:
            spine.set_visible(False)

    fig.tight_layout()
    return fig


def create_accumulated_depreciation_chart(df: pd.DataFrame) -> plt.Figure:
    """Create a stacked bar chart showing accumulated depreciation percentage.
    
    Each bar shows stacked segments representing each year's depreciation contribution.
    
    Args:
        df: DataFrame with 'year', 'prediction', and 'depreciation' columns
        
    Returns:
        Matplotlib figure
    """
    fig, ax = plt.subplots()
    fig.patch.set_facecolor("#181B23")
    ax.set_facecolor("#181B23")
    
    # Calculate yearly depreciation percentages relative to initial value
    base_val = float(df["prediction"].iloc[0]) if not df["prediction"].empty else 0.0
    df_copy = df.copy()
    df_copy['depreciation_pct'] = (df_copy['depreciation'] / base_val * 100) if base_val != 0 else 0
    
    # Create blue gradient colors (lighter to darker)
    n_years = len(df_copy)
    blues = plt.cm.Blues(range(80, 256, (256-80)//max(n_years, 1)))
    
    # For each year position on x-axis, stack all depreciations up to that year
    years = df_copy['year'].tolist()
    totals = []  # Store total height for each bar
    for year_idx in range(len(years)):
        if year_idx == 0:
            totals.append(0)
            continue  # Skip first year (no depreciation yet)
        # Stack all depreciations from year 1 to current year
        bottom = 0
        for stack_idx in range(1, year_idx + 1):
            height = df_copy.iloc[stack_idx]['depreciation_pct']
            ax.bar(years[year_idx], height, bottom=bottom, color=blues[stack_idx], 
                   edgecolor='white', linewidth=0.5, width=0.6)
            bottom += height
        totals.append(bottom)
    # Add total depreciation labels on top of each bar
    for year_idx, (year, total) in enumerate(zip(years, totals)):
        if total > 0:
            ax.text(year, total, f"{total:.1f}%", ha='center', va='bottom', 
                    fontsize=10, fontweight='regular', color='white')
    ax.set_xlabel("Year (age)", color="white")
    ax.set_ylabel("Accumulated depreciation (%)", color="white")
    ax.set_title("Accumulated depreciation (%) - Stacked by year contributions", color="white")
    ax.set_xticks(years)
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    
    # Set axis spine colors to white and hide top/right
    for position, spine in ax.spines.items():
        spine.set_color('white')
        if position in ["top", "right"]:
            spine.set_visible(False)

    fig.tight_layout()
    return fig


def create_dual_axis_chart(df: pd.DataFrame) -> plt.Figure:
    """Create a dual-axis chart with annual depreciation % (line) and vehicle value (bars).
    
    Args:
        df: DataFrame with 'year', 'prediction', and 'depreciation_pct' columns
        
    Returns:
        Matplotlib figure
    """
    fig, ax1 = plt.subplots()
    fig.patch.set_facecolor("#181B23")
    ax1.set_facecolor("#181B23")
    
    # Right axis: Vehicle value as bar chart (plot first, so it's in background)
    ax2 = ax1.twinx()
    color_bar = 'tab:blue'
    ax2.set_ylabel('Vehicle value', color='white')
    bars = ax2.bar(df['year'], df['prediction'], color=color_bar, alpha=0.6, width=0.6, zorder=1)
    ax2.tick_params(axis='y', labelcolor='white', colors='white')
    # Add value labels on bars with dot formatting
    for idx, (year, value) in enumerate(zip(df['year'], df['prediction'])):
        label = f"{value:,.0f}".replace(",", ".")
        ax2.text(year, value, label, ha='center', va='bottom', fontsize=9, color='white')
    # Left axis: Annual depreciation % as line chart (plot second, so it's on top)
    color_line = 'tab:orange'
    ax1.set_xlabel('Year (age)', color='white')
    ax1.set_ylabel('Annual depreciation (%)', color='white')
    ax1.plot(df['year'], df['depreciation_pct'], color=color_line, marker='o', 
             linewidth=2.5, label='Annual depreciation %', zorder=2)
    ax1.tick_params(axis='y', labelcolor='white', colors='white')
    ax1.tick_params(axis='x', colors='white')
    ax1.grid(True, alpha=0.3, zorder=0)
    ax1.set_zorder(ax2.get_zorder() + 1)  # Ensure ax1 is on top
    ax1.patch.set_visible(False)  # Make ax1 background transparent
    plt.title('Annual Depreciation % vs Vehicle Value', color='white')
    
    # Configure spines for both axes
    for ax in [ax1, ax2]:
        for position, spine in ax.spines.items():
            spine.set_color('white')
            if position == "top":
                spine.set_visible(False)

    fig.tight_layout()
    return fig


def build_comparison_data(
    years: List[int],
    comparison_values: List[str],
    comparison_key: str,
    base_payload: dict,
    avg_km_per_year: int,
    predict_func,
    model_path: str,
    explicit_kms: List[int] = None
) -> pd.DataFrame:
    """Build comparison data for fuel types or brands.
    
    Args:
        years: List of years to predict for
        comparison_values: List of values to compare (fuel types or brands)
        comparison_key: Key name in payload ('fuel_type' or 'brand')
        base_payload: Base payload with other parameters
        avg_km_per_year: Average kilometers per year
        predict_func: Prediction function to use
        model_path: Path to the model
        explicit_kms: Optional list of KMs corresponding to years. If provided, overrides avg_km_per_year logic.
        
    Returns:
        DataFrame with comparison data
    """
    import json
    
    rows = []
    for val in comparison_values:
        payloads = []
        for i, y in enumerate(years):
            payload = base_payload.copy()
            
            if explicit_kms is not None and i < len(explicit_kms):
                payload["km"] = explicit_kms[i]
            else:
                payload["km"] = int(round(y * avg_km_per_year))
                
            payload["age"] = int(y)
            payload[comparison_key] = val
            payloads.append(payload)
        
        preds = predict_func(json.dumps(payloads, sort_keys=True), model_path)
        for y, p in zip(years, preds):
            rows.append({comparison_key: val, "year": y, "prediction": p})
    
    return pd.DataFrame(rows)
