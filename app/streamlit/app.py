import streamlit as st
from utils.ui_theme import set_page_meta, inject_sidebar_styles, inject_play_font, inject_metric_styles
from utils.analytics import inject_microsoft_clarity

# Set page metadata and inject shared UI styles before pages render
set_page_meta("Car Value Predictor", icon="app/streamlit/assets/icons/favicon.ico")
# Apply self-hosted Play font globally
inject_play_font()
inject_sidebar_styles()
inject_metric_styles()
# Add Microsoft Clarity analytics
inject_microsoft_clarity()

# Define pages with custom titles
predictor_page = st.Page("pages/predictor.py", title="🚗 Predictor 📉")
context_page = st.Page("pages/context.py", title="💡 Project Context 📋")

# Create navigation
pg = st.navigation([predictor_page, context_page])

# Run the selected page
pg.run()
