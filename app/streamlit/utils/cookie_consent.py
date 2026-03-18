"""Cookie consent modal popup for analytics compliance (GDPR/CCPA).

Displays a centered modal overlay informing users about cookie usage
and allows them to accept or decline analytics tracking.
"""

from __future__ import annotations

import streamlit as st
from typing import Optional


def get_consent_status() -> Optional[bool]:
    """Get the current cookie consent status from session state.
    
    Returns:
        True if accepted, False if declined, None if not yet decided
    """
    return st.session_state.get("cookie_consent", None)  # type: ignore[attr-defined]


def set_consent_status(accepted: bool) -> None:
    """Store cookie consent decision in session state.
    
    Args:
        accepted: True if user accepts cookies, False if declined
    """
    st.session_state["cookie_consent"] = accepted  # type: ignore[attr-defined]


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
    
    **Your choice will apply for this session.**
    """
    st.markdown(content)  # type: ignore[attr-defined]
    
    col1, col2, col3 = st.columns([1, 1, 1])  # type: ignore[attr-defined]
    
    with col1:
        st.write("")  # type: ignore[attr-defined] - Spacer
    
    with col2:
        if st.button("✓ Accept Cookies", type="primary", width="stretch"):  # type: ignore[attr-defined]
            set_consent_status(True)
            st.rerun()  # type: ignore[attr-defined]
    
    with col3:
        if st.button("✗ Decline", width="stretch"):  # type: ignore[attr-defined]
            set_consent_status(False)
            st.rerun()  # type: ignore[attr-defined]


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
