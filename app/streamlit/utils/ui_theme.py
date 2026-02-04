"""UI theme helpers for the Streamlit app.

Place global `st.markdown` CSS injections here and call
`inject_sidebar_styles()` from `app.py` before pages render.
"""

import streamlit as st


def inject_sidebar_styles() -> None:
    """Inject sidebar CSS to align navigation item styles with the Filters heading.

    This keeps styling centralized and easy to maintain.
    """
    st.markdown("""
        <style>
        /* Explicitly set Filters heading and nav items to the same size so they match */
        section[data-testid="stSidebar"] h2 {
            font-size: 1.25rem !important;
            font-weight: 700 !important;
            margin-bottom: 0.5rem !important;
        }
        /* Basic spacing for nav items; explicit size below ensures matching */
        section[data-testid="stSidebar"] ul li button,
        section[data-testid="stSidebar"] ul li a {
            padding-top: 0.25rem !important;
            padding-bottom: 0.25rem !important;
            min-height: 40px !important;
        }
        section[data-testid="stSidebar"] ul li button span,
        section[data-testid="stSidebar"] ul li a span {
            display: inline-flex !important;
            align-items: center !important;
            gap: 0.4rem !important;
            font-size: 1.25rem !important;
            font-weight: 700 !important;
        }
        </style>
    """, unsafe_allow_html=True)


def inject_metric_styles() -> None:
    """Inject CSS to center metric labels and values, and bold labels.

    Designed for Streamlit 1.52.x `st.metric` markup.
    Does not change the default metric value font size.
    """
    st.markdown(
        """
        <style>
        /* Streamlit 1.52.x: make metric stretch full width so centering works */
        div[data-testid="stMetric"] {
            width: 100% !important;
            display: flex !important;
            flex-direction: column !important;
            align-items: stretch !important;
            text-align: center !important;
        }

        /* Center + bold the metric label (header) */
        div[data-testid="stMetric"] [data-testid="stMetricLabel"],
        div[data-testid="stMetricLabel"] {
            width: 100% !important;
            align-self: stretch !important;
            display: block !important;
            text-align: center !important;
            font-weight: 700 !important;
        }
        div[data-testid="stMetric"] [data-testid="stMetricLabel"] *,
        div[data-testid="stMetricLabel"] * {
            width: 100% !important;
            text-align: center !important;
            font-weight: 700 !important;
            margin-left: auto !important;
            margin-right: auto !important;
        }

        /* Center the metric value without changing default font-size */
        div[data-testid="stMetric"] [data-testid="stMetricValue"],
        div[data-testid="stMetricValue"] {
            width: 100% !important;
            align-self: stretch !important;
            display: block !important;
            text-align: center !important;
        }
        div[data-testid="stMetric"] [data-testid="stMetricValue"] *,
        div[data-testid="stMetricValue"] * {
            text-align: center !important;
            margin-left: auto !important;
            margin-right: auto !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def inject_global_styles(css: str) -> None:
    """Inject arbitrary global CSS into the app.

    Args:
        css: CSS string to inject (without surrounding <style> tags).
    """
    if not css:
        return
    wrapped = f"""<style>{css}</style>"""
    st.markdown(wrapped, unsafe_allow_html=True)


def inject_fonts(family: str, url: str = None) -> None:
    """Load a web font and apply it globally.

    Args:
        family: Font-family name to apply (e.g. 'Inter').
        url: Optional URL for @import or <link> to load the font.
    """
    if url:
        # Use @import to keep a single injection point
        st.markdown(f"""<style>@import url('{url}'); body {{ font-family: '{family}', sans-serif; }}</style>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""<style>body {{ font-family: '{family}', sans-serif; }}</style>""", unsafe_allow_html=True)


def inject_play_font() -> None:
    """Inject self-hosted Play font using @font-face and apply globally.
    
    Loads the Play font family (Regular and Bold) from local assets
    and applies it to all Streamlit UI elements.
    Checks config.USE_CUSTOM_FONT to determine if custom font should be applied.
    """
    from .config import USE_CUSTOM_FONT, CUSTOM_FONT_NAME, CUSTOM_FONT_PATHS
    
    if not USE_CUSTOM_FONT:
        return  # Use Streamlit's default font
    
    font_css = f'''
    @font-face {{
        font-family: '{CUSTOM_FONT_NAME}';
        src: url('{CUSTOM_FONT_PATHS["regular"]}') format('truetype');
        font-weight: 400;
        font-style: normal;
        font-display: swap;
    }}
    @font-face {{
        font-family: '{CUSTOM_FONT_NAME}';
        src: url('{CUSTOM_FONT_PATHS["bold"]}') format('truetype');
        font-weight: 700;
        font-style: normal;
        font-display: swap;
    }}
    /* Apply {CUSTOM_FONT_NAME} font globally across Streamlit containers */
    body, html, .stApp, .stApp * , .block-container, .block-container * , section[data-testid="stSidebar"], section[data-testid="stSidebar"] * {{
        font-family: '{CUSTOM_FONT_NAME}', sans-serif !important;
    }}
    /* Ensure headings and buttons use the bold face where appropriate */
    h1, h2, h3, h4, h5, h6, button, .stButton button {{
        font-family: '{CUSTOM_FONT_NAME}', sans-serif !important;
        font-weight: 700 !important;
    }}
    '''
    inject_global_styles(font_css)


def set_page_meta(title: str, icon: str | None = None, layout: str = "centered") -> None:
    """Convenience wrapper around `st.set_page_config`.

    Args:
        title: Page title for the browser tab.
        icon: Optional page icon (emoji or path).
        layout: Layout mode passed to Streamlit.
    """
    if icon:
        st.set_page_config(page_title=title, page_icon=icon, layout=layout)
    else:
        st.set_page_config(page_title=title, layout=layout)


def sidebar_heading(text: str, icon: str | None = None) -> None:
    """Render a consistent sidebar section heading.

    Args:
        text: Heading text
        icon: Optional emoji or icon to show before the text
    """
    if icon:
        st.sidebar.markdown(f"<h2 style='margin:0.2rem 0 0.6rem 0'>{icon} {text}</h2>", unsafe_allow_html=True)
    else:
        st.sidebar.markdown(f"<h2 style='margin:0.2rem 0 0.6rem 0'>{text}</h2>", unsafe_allow_html=True)


def footer(text: str) -> None:
    """Render a small footer caption at the bottom of the main area.

    Args:
        text: Footer text to display
    """
    st.caption(text)
