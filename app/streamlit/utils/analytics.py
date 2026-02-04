"""Analytics and tracking integrations for the Streamlit app.

This module handles third-party analytics tools like Microsoft Clarity.
"""

from __future__ import annotations

import html
import os
from typing import Optional

import streamlit as st


def _get_clarity_project_id() -> Optional[str]:
    project_id: Optional[str] = None

    # Prefer Streamlit secrets (e.g. .streamlit/secrets.toml or cloud secrets),
    # then fall back to environment variables (e.g. Docker/Coolify).
    try:
        project_id = st.secrets.get("CLARITY_PROJECT_ID")  # type: ignore[attr-defined]
    except Exception:
        project_id = None

    if not project_id:
        project_id = os.getenv("CLARITY_PROJECT_ID")

    if not project_id:
        return None

    project_id = str(project_id).strip()
    return project_id or None


def inject_microsoft_clarity(project_id: str | None = None) -> None:
    """Inject Microsoft Clarity analytics tracking script.

    The Clarity project ID is intentionally loaded from configuration so it
    doesn't need to live in the public repository.

    Configuration (checked in this order):
    - `project_id` argument
    - Streamlit secrets key `CLARITY_PROJECT_ID`
    - Environment variable `CLARITY_PROJECT_ID`
    """

    project_id = project_id or _get_clarity_project_id()
    if not project_id:
        return

    safe_project_id = html.escape(project_id, quote=True)
    clarity_script = f"""
    <script type="text/javascript">
        (function(c,l,a,r,i,t,y){{
            c[a]=c[a]||function(){{(c[a].q=c[a].q||[]).push(arguments)}};
            t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
            y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
        }})(window, document, "clarity", "script", "{safe_project_id}");
    </script>
    """
    st.components.v1.html(clarity_script, height=0)
