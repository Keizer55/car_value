"""Cookie consent banner for analytics compliance (GDPR/CCPA).

Displays a non-intrusive banner informing users about cookie usage
and allows them to accept or decline analytics tracking.
"""

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


def show_cookie_banner() -> None:
    """Display cookie consent banner if user hasn't decided yet.
    
    Shows a fixed bottom banner with information about cookie usage
    and action buttons. Only displays if consent status is None.
    """
    from .config import ENABLE_COOKIE_CONSENT
    
    if not ENABLE_COOKIE_CONSENT:
        # If consent is disabled, assume acceptance
        if get_consent_status() is None:
            set_consent_status(True)
        return
    
    consent_status = get_consent_status()
    
    # Don't show banner if user already decided
    if consent_status is not None:
        return
    
    # Inject cookie banner CSS and HTML
    banner_html = """
    <style>
    .cookie-banner {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: rgba(30, 30, 30, 0.98);
        color: #ffffff;
        padding: 1rem 1.5rem;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.2);
        z-index: 999999;
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 1rem;
        font-size: 0.9rem;
        backdrop-filter: blur(10px);
    }
    
    .cookie-banner-text {
        flex: 1;
        min-width: 250px;
        line-height: 1.5;
    }
    
    .cookie-banner-text a {
        color: #58a6ff;
        text-decoration: underline;
    }
    
    .cookie-banner-buttons {
        display: flex;
        gap: 0.75rem;
        align-items: center;
    }
    
    @media (max-width: 768px) {
        .cookie-banner {
            flex-direction: column;
            align-items: stretch;
            text-align: center;
        }
        .cookie-banner-buttons {
            justify-content: center;
        }
    }
    </style>
    
    <div class="cookie-banner">
        <div class="cookie-banner-text">
            🍪 This website uses cookies and analytics (Microsoft Clarity) to improve user experience. 
            We collect anonymized usage data to understand how visitors interact with our predictions. 
            <a href="https://privacy.microsoft.com/en-us/privacystatement" target="_blank" rel="noopener">Privacy Policy</a>
        </div>
        <div class="cookie-banner-buttons">
            <span style="color: #888; font-size: 0.85rem; margin-right: 0.5rem;">Your choice will apply for this session</span>
        </div>
    </div>
    """
    
    st.markdown(banner_html, unsafe_allow_html=True)  # type: ignore[attr-defined]
    
    # Action buttons in a container
    col1, col2, col3 = st.columns([4, 1, 1])  # type: ignore[attr-defined]
    
    with col2:
        if st.button("✓ Accept", key="cookie_accept", use_container_width=True):  # type: ignore[attr-defined]
            set_consent_status(True)
            st.rerun()  # type: ignore[attr-defined]
    
    with col3:
        if st.button("✗ Decline", key="cookie_decline", use_container_width=True):  # type: ignore[attr-defined]
            set_consent_status(False)
            st.rerun()  # type: ignore[attr-defined]


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
