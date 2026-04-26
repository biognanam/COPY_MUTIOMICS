"""Streamlit entry point for the Multi-Omics Biomarker Discovery Platform."""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from modules.auth import AuthManager
from modules.state import initialize_state, logout
from ui_pages.login_page import render_login_page
from ui_pages.workflow_page import render_workflow
from utils.constants import (
    APP_TAGLINE,
    APP_TITLE,
    CREATED_BY,
    PAGE_ACCESS,
    SUPERVISED_BY,
    WORKFLOW_PAGE,
)
from utils.theme import apply_theme


LOGO_PATH = Path(__file__).resolve().parent / "assets" / "biomarker_logo.svg"


st.set_page_config(
    page_title=APP_TITLE,
    page_icon="R",
    layout="wide",
    initial_sidebar_state="expanded",
)


def main() -> None:
    initialize_state()
    apply_theme(login_screen=not st.session_state.authenticated)

    auth_manager = AuthManager()

    if not st.session_state.authenticated:
        render_login_page(auth_manager)
        return

    role = st.session_state.role
    available_pages = PAGE_ACCESS.get(role, [WORKFLOW_PAGE])
    if WORKFLOW_PAGE not in available_pages:
        st.error("This account is not authorized for the workflow page.")
        return

    with st.sidebar:
        if LOGO_PATH.exists():
            _, logo_center, _ = st.columns([1.2, 2.4, 1.2])
            with logo_center:
                st.image(str(LOGO_PATH), width=98)

        st.markdown(f"<div class='sidebar-brand'>{APP_TITLE}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='sidebar-tagline'>{APP_TAGLINE}</div>", unsafe_allow_html=True)
        st.markdown("---")

        with st.expander("Settings", expanded=False):
            st.markdown(f"**User:** {st.session_state.username}")
            st.markdown(f"**Role:** {role.title()}")
            st.markdown(f"**{CREATED_BY}**")
            st.markdown(SUPERVISED_BY)

        if role == "clinician":
            st.info("Clinician mode: view-only workflow and report interpretation.")

        st.markdown("---")
        st.markdown("**Workflow**")
        st.caption("Ingestion -> QC -> Integration -> AI Modeling -> Pathway -> Validation -> Report")

        st.markdown("---")
        st.markdown("<div class='small-note'>For research use only. Not for direct clinical diagnosis.</div>", unsafe_allow_html=True)

        if st.button("Logout", use_container_width=True):
            logout()
            st.rerun()

    render_workflow()


if __name__ == "__main__":
    main()
