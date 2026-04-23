"""Search history page — session-based."""

import pytz
import streamlit as st
from datetime import datetime

from config.settings import DISPLAY_TIMEZONE


def render_history_page():
    """Render the search history page."""
    st.header("Suchverlauf")

    history = st.session_state.get("search_history", [])

    if not history:
        st.info("Noch keine Suchanfragen in dieser Sitzung.")
        return

    col1, col2 = st.columns([4, 1])
    with col2:
        if st.button("Verlauf löschen"):
            st.session_state["search_history"] = []
            st.rerun()

    berlin = pytz.timezone(DISPLAY_TIMEZONE)

    for i, entry in enumerate(history):
        col1, col2, col3, col4 = st.columns([3, 2, 1, 1])

        with col1:
            st.markdown(f"**{entry['query']}**")

        with col2:
            t = entry.get("time", "")
            if t:
                try:
                    dt = datetime.fromisoformat(t)
                    dt_berlin = dt.astimezone(berlin)
                    st.caption(dt_berlin.strftime("%d.%m.%Y %H:%M"))
                except (ValueError, TypeError):
                    st.caption(t)

        with col3:
            st.caption(f"{entry.get('count', 0)} Treffer")

        with col4:
            if st.button("Suchen", key=f"hist_{i}", help="Erneut suchen"):
                st.session_state["search_query"] = entry["query"]
                st.session_state["nav"] = "Suche"
                st.rerun()
