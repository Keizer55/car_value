"""Cookie consent modal popup for analytics compliance (GDPR/CCPA).

Displays a centered modal overlay informing users about cookie usage
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
    """Display cookie consent modal popup if user hasn't decided yet.
    
    Shows a centered modal overlay with information about cookie usage
    and action buttons. Only displays if consent status is None.
    """
    from .config import ENABLE_COOKIE_CONSENT
    
    if not ENABLE_COOKIE_CONSENT:
        # If consent is disabled, assume acceptance
        if get_consent_status() is None:
            set_consent_status(True)
        return
    
    consent_status = get_consent_status()
    
    # Don't show modal if user already decided
    if consent_status is not None:
        return
    
    # Create modal popup with action buttons
    modal_html = """
    <style>
    .cookie-modal-overlay {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.7);
        backdrop-filter: blur(4px);
        z-index: 999998;
        display: flex;
        align-items: center;
        justify-content: center;
        animation: fadeIn 0.3s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes slideUp {
        from { 
            opacity: 0;
            transform: translateY(30px);
        }
        to { 
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .cookie-modal {
        background: linear-gradient(135deg, #1e3a8a 0%, #1e1e1e 100%);
        border: 2px solid rgba(88, 166, 255, 0.3);
        border-radius: 16px;
        padding: 2rem;
        max-width: 500px;
        width: 90%;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
        color: #ffffff;
        animation: slideUp 0.4s ease-out;
        position: relative;
    }
    
    .cookie-modal-icon {
        font-size: 3rem;
        text-align: center;
        margin-bottom: 1rem;
        animation: bounce 2s infinite;
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    .cookie-modal-title {
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        text-align: center;
        color: #58a6ff;
    }
    
    .cookie-modal-text {
        font-size: 0.95rem;
        line-height: 1.6;
        margin-bottom: 1.5rem;
        text-align: center;
        color: #e0e0e0;
    }
    
    .cookie-modal-text a {
        color: #58a6ff;
        text-decoration: underline;
        font-weight: 600;
    }
    
    .cookie-modal-text a:hover {
        color: #79b8ff;
    }
    
    .cookie-modal-buttons {
        display: flex;
        gap: 1rem;
        justify-content: center;
        margin-top: 1.5rem;
    }
    
    .cookie-btn {
        padding: 0.75rem 2rem;
        border: none;
        border-radius: 8px;
        font-size: 1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        min-width: 120px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .cookie-btn-accept {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4);
    }
    
    .cookie-btn-accept:hover {
        background: linear-gradient(135deg, #059669 0%, #047857 100%);
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.6);
        transform: translateY(-2px);
    }
    
    .cookie-btn-decline {
        background: linear-gradient(135deg, #6b7280 0%, #4b5563 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(107, 114, 128, 0.4);
    }
    
    .cookie-btn-decline:hover {
        background: linear-gradient(135deg, #4b5563 0%, #374151 100%);
        box-shadow: 0 6px 20px rgba(107, 114, 128, 0.6);
        transform: translateY(-2px);
    }
    
    .cookie-info {
        font-size: 0.8rem;
        color: #9ca3af;
        text-align: center;
        margin-top: 1rem;
        font-style: italic;
    }
    
    @media (max-width: 600px) {
        .cookie-modal {
            padding: 1.5rem;
            width: 95%;
        }
        
        .cookie-modal-buttons {
            flex-direction: column;
        }
        
        .cookie-btn {
            width: 100%;
        }
    }
    </style>
    
    <div class="cookie-modal-overlay" id="cookieModalOverlay">
        <div class="cookie-modal">
            <div class="cookie-modal-icon">🍪</div>
            <div class="cookie-modal-title">Cookie Consent</div>
            <div class="cookie-modal-text">
                This website uses cookies and analytics (Microsoft Clarity) to improve your experience.
                We collect anonymized usage data to understand how visitors interact with our predictions.
                <br><br>
                <a href="https://privacy.microsoft.com/en-us/privacystatement" target="_blank" rel="noopener">View Privacy Policy</a>
            </div>
            <div class="cookie-modal-buttons">
                <button class="cookie-btn cookie-btn-accept" onclick="handleCookieConsent(true)">
                    ✓ Accept
                </button>
                <button class="cookie-btn cookie-btn-decline" onclick="handleCookieConsent(false)">
                    ✗ Decline
                </button>
            </div>
            <div class="cookie-info">
                Your choice will apply for this session
            </div>
        </div>
    </div>
    
    <script>
    function handleCookieConsent(accepted) {
        // Store decision in sessionStorage for immediate feedback
        sessionStorage.setItem('cookieConsent', accepted ? 'accepted' : 'declined');
        
        // Hide modal immediately for better UX
        const overlay = document.getElementById('cookieModalOverlay');
        if (overlay) {
            overlay.style.animation = 'fadeOut 0.2s ease-out';
            overlay.style.opacity = '0';
            setTimeout(() => overlay.remove(), 200);
        }
        
        // Trigger Streamlit rerun by dispatching custom event
        // Streamlit will detect the query param change and rerun
        const currentUrl = new URL(window.location.href);
        currentUrl.searchParams.set('cookie_consent', accepted ? 'accept' : 'decline');
        currentUrl.searchParams.set('_t', Date.now()); // Cache buster
        window.location.href = currentUrl.toString();
    }
    
    @keyframes fadeOut {
        from { opacity: 1; }
        to { opacity: 0; }
    }
    </script>
    """
    
    st.components.v1.html(modal_html, height=0)  # type: ignore[attr-defined]
    
    # Check for query parameter from JavaScript redirect
    try:
        query_params = st.query_params  # type: ignore[attr-defined]
        cookie_consent_param = query_params.get("cookie_consent", [None])[0] if isinstance(query_params.get("cookie_consent"), list) else query_params.get("cookie_consent")
        
        if cookie_consent_param == "accept":
            set_consent_status(True)
            # Clear query params and rerun
            st.query_params.clear()  # type: ignore[attr-defined]
            st.rerun()  # type: ignore[attr-defined]
        elif cookie_consent_param == "decline":
            set_consent_status(False)
            # Clear query params and rerun
            st.query_params.clear()  # type: ignore[attr-defined]
            st.rerun()  # type: ignore[attr-defined]
    except Exception:
        # Fallback: query_params might not be available in older Streamlit versions
        pass


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
