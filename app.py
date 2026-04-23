"""FilmFinder — German TV Program Search App (stateless version)."""

import logging
import streamlit as st

from src.ui.pages.favorites import render_favorites_page
from src.ui.pages.history import render_history_page
from src.ui.pages.search import render_search_page

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

st.set_page_config(
    page_title="FilmFinder",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Sidebar navigation
st.sidebar.title("FilmFinder")
st.sidebar.caption("Deutsches TV-Programm durchsuchen")

pages = {
    "Suche": "🔍",
    "Favoriten": "⭐",
    "Suchverlauf": "📜",
}

default_page = st.session_state.pop("nav", "Suche")
if default_page not in pages:
    default_page = "Suche"

selected = st.sidebar.radio(
    "Navigation",
    list(pages.keys()),
    index=list(pages.keys()).index(default_page),
    format_func=lambda x: f"{pages[x]} {x}",
    label_visibility="collapsed",
)

if selected == "Suche":
    render_search_page()
elif selected == "Favoriten":
    render_favorites_page()
elif selected == "Suchverlauf":
    render_history_page()
