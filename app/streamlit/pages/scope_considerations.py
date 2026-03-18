import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from utils.config import BASE_DIR
from utils.ui_theme import footer, sidebar_heading


def render_section(title: str, body: str, icon: str) -> None:
    """Render a consistently styled content section."""
    with st.container(border=True):
        st.markdown(f"### {icon} {title}")
        st.markdown(body)


st.title("Scope & Considerations")

st.markdown(
    """
<style>
.scope-hero {
    padding: 1rem 1.1rem;
    border-radius: 14px;
    border: 1px solid #d9e3f0;
    background: linear-gradient(135deg, #f5f9ff 0%, #eef5ea 100%);
    margin-bottom: 0.75rem;
}
.scope-note {
    margin-top: 0.5rem;
    padding: 0.55rem 0.75rem;
    border-left: 4px solid #2b7a78;
    background: #f2f8f7;
    border-radius: 8px;
    font-size: 0.92rem;
}
</style>

<div class="scope-hero">
<h3 style="margin:0 0 0.35rem 0;">Scope and Considerations of the Analysis</h3>

This project has a clear objective: to serve as a qualitative reference built on real data. Over <b>15,000 second-hand car listings</b> from the Spanish market were captured to build a value estimation model and visualize depreciation trends.

The results are indicative and should be interpreted as an analytical approximation, not a precise financial valuation.

The analysis allows exploration of how a vehicle's price varies according to variables such as year, mileage, brand, or model. However, every simplification comes with considerations worth keeping in mind.
</div>
""",
    unsafe_allow_html=True,
)

col_1, col_2, col_3 = st.columns(3)
col_1.metric("Listings analyzed", "15,000+")
col_2.metric("Inflation period", "2010-2025")
col_3.metric("Highest annual CPI", "+8.4% (2022)")

st.markdown(
    """
<div class="scope-note">
Interpretation tip: this page provides methodological context so model outputs are read as market signals, not exact transactional values.
</div>
""",
    unsafe_allow_html=True,
)

render_section(
    "1) Technological Evolution of the Vehicle Over Time",
    """
When comparing a **2015 VW Golf** with a **2024 VW Golf**, the product itself has changed substantially. Newer generations include major advances in safety (ADAS, automatic braking), efficiency, connectivity, and comfort.

That means part of the observed price difference is not pure depreciation, but a **quality and product-generation gap**.

In the current analysis, all cars within the same model line are treated as homogeneous, even though they may belong to different generations or facelifts.
""",
    "🚘",
)

image_path = BASE_DIR / "docs" / "Gemini_Generated_Image_2d61s62d61s62d61.png"
if image_path.exists():
    st.image(str(image_path), width="stretch")
else:
    st.info("Reference image not found in docs folder.")

render_section(
    "2) Inflation Is Not Accounted For (Nominal vs Real)",
    """
All prices are modeled in **nominal terms** (current euros), without inflation adjustment.

A car that cost 20,000 EUR in 2015 and is worth 14,000 EUR today appears to have lost 30%. But if accumulated inflation since 2015 is around 25%, real depreciation is much smaller, and in some cases real value can even be higher than expected.

This effect became especially relevant after the **2022 inflation spike (+8.4%)**. Spain's accumulated inflation from 2010 to 2025 is approximately **44%**.

A car bought in 2010 at 15,000 EUR would need to be around **21,600 EUR** in 2025 just to preserve equivalent purchasing power.
""",
    "📈",
)

inflation_rows = [
    (2010, 2.0, "Post-crisis recovery"),
    (2011, 3.2, "Energy and commodity surge"),
    (2012, 2.4, "Austerity period"),
    (2013, 1.4, "Growth slowdown"),
    (2014, -0.2, "Deflationary pressure"),
    (2015, -0.5, "Deflation trough"),
    (2016, -0.2, "Low oil prices"),
    (2017, 2.0, "Recovery begins"),
    (2018, 1.7, "Stable growth"),
    (2019, 0.7, "Subdued inflation"),
    (2020, -0.3, "COVID-19 demand collapse"),
    (2021, 3.1, "Post-COVID rebound"),
    (2022, 8.4, "Energy crisis peak"),
    (2023, 3.5, "Gradual normalization"),
    (2024, 2.8, "Approaching ECB target"),
    (2025, 2.9, "Stabilization"),
]

inflation_df = pd.DataFrame(inflation_rows, columns=["Year", "Inflation", "Context"])


import numpy as np
# Custom color logic: positive = red gradient, negative = green, 0 = split
reds_cmap = plt.colormaps["Reds"]
greens_cmap = plt.colormaps["Greens"]
min_inf = inflation_df["Inflation"].min()
max_inf = inflation_df["Inflation"].max()
bar_colors = []
for v in inflation_df["Inflation"]:
    if v > 0:
        # Normalize positive inflation to [0,1] and use lighter reds
        norm = (v - 0) / (max_inf - 0) if max_inf != 0 else 0
        bar_colors.append(reds_cmap(0.15 + norm * 0.4))
    elif v < 0:
        # Normalize negative inflation to [0,1] and use lighter greens
        norm = (v - min_inf) / (0 - min_inf) if min_inf != 0 else 0
        bar_colors.append(greens_cmap(0.15 + norm * 0.4))
    else:
        bar_colors.append("#cccccc")  # Neutral gray for zero

fig, ax = plt.subplots(figsize=(12, 5))
fig.patch.set_facecolor("#181B23")
ax.set_facecolor("#181B23")

ax.bar(inflation_df["Year"], inflation_df["Inflation"], color=bar_colors, edgecolor="#222", linewidth=0.7)
# Draw average inflation line
avg_inflation = inflation_df["Inflation"].mean()
ax.axhline(avg_inflation, color="#1f77b4", linestyle="--", linewidth=1.6, label=f"Average ({avg_inflation:.2f}%)")
ax.axhline(0, color="#cccccc", linewidth=1)

for year, value in zip(inflation_df["Year"], inflation_df["Inflation"]):
    y_offset = 0.16 if value >= 0 else -0.22
    vertical_align = "bottom" if value >= 0 else "top"
    ax.text(year, value + y_offset, f"{value:+.1f}%", ha="center", va=vertical_align, fontsize=9, color="white")

ax.set_title("Spain CPI (2010-2025): Annual Inflation", pad=10, color="white")
ax.set_ylabel("Annual CPI (%)", color="white")
ax.set_xlabel("Year", color="white")
ax.set_xticks(inflation_df["Year"])
ax.tick_params(axis="x", rotation=45, colors="white")
ax.tick_params(axis="y", colors="white")
ax.grid(axis="y", linestyle="--", alpha=0.18)
ax.legend(frameon=False, labelcolor="white")
# Set axis spine colors to white and hide top/right
for position, spine in ax.spines.items():
    spine.set_color('white')
    if position in ["top", "right"]:
        spine.set_visible(False)
fig.tight_layout()

st.caption("Color scale: lower and negative inflation in green, higher inflation in red.")
st.pyplot(fig, width="stretch")
st.caption("Color scale: lower and negative inflation in green, higher inflation in red.")

with st.expander("Inflation timeline details"):
    st.dataframe(
        inflation_df,
        width="stretch",
        hide_index=True,
        column_config={"Inflation": st.column_config.NumberColumn(format="%.1f%%")},
    )

render_section(
    "3) Current Price Comparisons Are Not Historical Depreciation",
    """
This is a key conceptual limitation. The dataset captures second-hand market prices at a single point in time (cross-section).

If a 10-year-old car is 50% cheaper than today's new equivalent, that does **not** mean the same unit depreciated exactly 50% over 10 years.

Reasons:

- The older unit was sold new in a different period with a different original list price.
- True depreciation requires comparing current used price against original catalogue price, adjusted for inflation.
- That original list price is not available in second-hand listing platforms.
""",
    "🧭",
)

render_section(
    "4) Point-in-Time Snapshot (Temporal Bias)",
    """
The data was captured on a single date, which introduces seasonality and macroeconomic bias.

Examples:

- Seasonality can shift supply and demand by vehicle type (for example, more convertibles listed in autumn/winter and stronger SUV demand in specific periods).
- Semiconductor shortages (2021-2023) created anomalous periods in which second-hand prices spiked.
- Regulatory shifts (such as Low Emission Zones in Spain) can suppress prices for specific engines.
""",
    "🕒",
)

render_section(
    "5) Heterogeneity Within the Same Model",
    """
The analysis intentionally prioritizes mass-market generalist brands (Volkswagen, Toyota, Seat, Renault, etc.) because they have broader supply and more stable pricing behavior.

Even so, within the same model and year, prices may vary substantially by trim, engine, and condition.

This is amplified in premium brands (BMW, Mercedes, Audi, Porsche), where:

- Engine variants under the same model name can imply very different prices.
- High-end packages (M Sport, AMG Line, RS, etc.) can add significant value.
- Residual value dispersion is structurally larger.

As a consequence, model outputs are generally more reliable for generalist vehicles than for luxury segments.
""",
    "🧩",
)

render_section(
    "6) Listed Price vs Final Transaction Price",
    """
Collected prices are listing prices, not final transaction prices. In real transactions, negotiation often reduces the final amount.

There is also selection bias in one-day snapshots:

- Competitively priced vehicles sell faster and are less likely to appear.
- Overpriced vehicles remain listed longer and are overrepresented.

This can cause a mild upward bias in observed prices versus actual closed-sale values.
""",
    "💶",
)

footer("Methodological notes for interpretation of model outputs and market signals.")
