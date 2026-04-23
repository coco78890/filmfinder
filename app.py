"""FilmFinder — German TV Program Search App (stateless version)."""

import logging
import streamlit as st

from src.ui.pages.search import render_search_page

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

st.set_page_config(
    page_title="FilmFinder",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Hide the sidebar completely
st.markdown(
    "<style>[data-testid='stSidebar']{display:none}</style>",
    unsafe_allow_html=True,
)

render_search_page()
