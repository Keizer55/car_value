"""Cookie consent modal popup for analytics compliance (GDPR/CCPA).

Displays a centered modal overlay informing users about cookie usage
and allows them to accept or decline analytics tracking.
"""

from __future__ import annotations

import streamlit as st
from typing import Optional
import extra_streamlit_components as stx


# We no longer cache the cookie manager. Initializing it inside a cached function
# causes CachedWidgetWarning because it inherently uses Streamlit components/widgets.
def get_cookie_manager():
    # Only initialize the CookieManager once per session using session_state
    if "cookie_manager" not in st.session_state:
        st.session_state["cookie_manager"] = stx.CookieManager(key="cookie_manager_init")
    return st.session_state["cookie_manager"]


def get_consent_status() -> Optional[bool]:
    """Get the current cookie consent status from browser cookies.
    
    Returns:
        True if accepted, False if declined, None if not yet decided
    """
    cookie_manager = get_cookie_manager()
    
    # Check if we just set it in this session to avoid waiting for frontend sync
    if "_cookie_consent_choice" in st.session_state:
        val = st.session_state["_cookie_consent_choice"]
        if st.session_state.get("_cookie_consent_action_pending"):
            cookie_manager.set("cookie_consent", val, key="set_consent", max_age=365*24*60*60)
            st.session_state["_cookie_consent_action_pending"] = False
        return val == "true"

    status = cookie_manager.get(cookie="cookie_consent")
    
    # Cookie is stored as a string
    if status == "true":
        return True
    elif status == "false":
        return False
    return None


def set_consent_status(accepted: bool) -> None:
    """Queue cookie consent decision in session state. 
    It will be persisted to browser cookies on the next render pass.
    
    Args:
        accepted: True if user accepts cookies, False if declined
    """
    st.session_state["_cookie_consent_choice"] = "true" if accepted else "false"
    st.session_state["_cookie_consent_action_pending"] = True


@st.dialog("🍪 Cookie Consent")  # type: ignore[misc]
def show_cookie_consent_dialog() -> None:
    """Display cookie consent dialog using Streamlit's native dialog."""
    
    # Add custom styling for the dialog
    dialog_style = """
    <style>
    [data-testid="stDialog"] {
        background: linear-gradient(135deg, rgba(30, 58, 138, 0.95) 0%, rgba(30, 30, 30, 0.95) 100%);
    }
    </style>
    """
    st.markdown(dialog_style, unsafe_allow_html=True)  # type: ignore[attr-defined]
    
    content = """
    ### 🔒 Privacy Notice
    
    This website uses **cookies** and **analytics** (Microsoft Clarity) to improve your experience.
    
    We collect anonymized usage data to understand how visitors interact with our car value predictions.
    
    📄 [View Microsoft Privacy Policy](https://privacy.microsoft.com/en-us/privacystatement)
    
    ---
    
    **Your choice will be saved across sessions.**
    """
    st.markdown(content)  # type: ignore[attr-defined]
    
    col1, col2, col3 = st.columns([1, 1, 1])  # type: ignore[attr-defined]
    
    with col1:
        st.write("")  # type: ignore[attr-defined] - Spacer
    
    with col2:
        if st.button("✓ Accept Cookies", type="primary", width="stretch"):  # type: ignore[attr-defined]
            set_consent_status(True)
            st.rerun()  # forces app to rerun, pick up session state, and persist cookie
    
    with col3:
        if st.button("✗ Decline", width="stretch"):  # type: ignore[attr-defined]
            set_consent_status(False)
            st.rerun()  # forces app to rerun, pick up session state, and persist cookie


def show_cookie_banner() -> None:
    """Display cookie consent modal if user hasn't decided yet.
    
    Shows a native Streamlit dialog for cookie consent.
    Only displays if consent status is None.
    """
    from .config import ENABLE_COOKIE_CONSENT
    
    if not ENABLE_COOKIE_CONSENT:
        # If consent is disabled, assume acceptance
        if get_consent_status() is None:
            set_consent_status(True)
        return
    
    consent_status = get_consent_status()
    
    # Show dialog if user hasn't decided
    if consent_status is None:
        show_cookie_consent_dialog()


def should_load_analytics() -> bool:
    """Check if analytics should be loaded based on consent.
    
    Returns:
        True if analytics can be loaded, False otherwise
    """
    from .config import ENABLE_COOKIE_CONSENT
    
    if not ENABLE_COOKIE_CONSENT:
        # If consent system is disabled, allow analytics
        return True
    
    consent_status = get_consent_status()
    
    # Only load analytics if explicitly accepted
    # If None (not decided), don't load (strict GDPR compliance)
    return consent_status is True
