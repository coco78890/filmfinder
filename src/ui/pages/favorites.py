"""Favorites page — session-based favorites management."""

import pytz
import streamlit as st
from datetime import datetime

from config.settings import DISPLAY_TIMEZONE
from src.search.engine import search


def render_favorites_page():
    """Render the favorites page."""
    st.header("Favoriten")

    favs = st.session_state.get("favorites", [])

    if not favs:
        st.info("Noch keine Favoriten gespeichert. Fügen Sie welche über die Suche hinzu.")
        return

    # Add new favorite
    with st.expander("Neuen Favoriten hinzufügen"):
        col1, col2 = st.columns([3, 1])
        with col1:
            new_fav = st.text_input("Suchbegriff", key="new_fav_input", placeholder="z.B. Tatort")
        with col2:
            st.write("")
            st.write("")
            if st.button("Hinzufügen", key="add_fav_btn"):
                if new_fav.strip() and new_fav.strip() not in favs:
                    favs.append(new_fav.strip())
                    st.session_state["favorites"] = favs
                    st.rerun()

    cached = st.session_state.get("cached_listings", [])
    berlin = pytz.timezone(DISPLAY_TIMEZONE)

    for i, fav_query in enumerate(favs):
        with st.container():
            col1, col2, col3 = st.columns([4, 1, 1])

            with col1:
                st.markdown(f"**{fav_query}**")

            with col2:
                if st.button("Suchen", key=f"search_fav_{i}", help="Jetzt suchen"):
                    st.session_state["search_query"] = fav_query
                    st.session_state["nav"] = "Suche"
                    st.rerun()

            with col3:
                if st.button("Entfernen", key=f"del_fav_{i}"):
                    favs.remove(fav_query)
                    st.session_state["favorites"] = favs
                    st.rerun()

            # Show quick matches from cached listings
            if cached:
                matches = search(query=fav_query, listings=cached, enrich_from_api=False, threshold=70)
                if matches:
                    match_data = []
                    for m in matches[:5]:
                        start = m.get("start_time", "")
                        date_str = ""
                        time_str = ""
                        if start:
                            try:
                                dt = datetime.fromisoformat(start)
                                dt_berlin = dt.astimezone(berlin)
                                date_str = dt_berlin.strftime("%d.%m.%Y")
                                time_str = dt_berlin.strftime("%H:%M")
                            except (ValueError, TypeError):
                                pass
                        match_data.append({
                            "Sender": m.get("channel", ""),
                            "Datum": date_str,
                            "Uhrzeit": time_str,
                            "Titel": m.get("title", ""),
                        })
                    st.dataframe(match_data, use_container_width=True, hide_index=True)
                else:
                    st.caption("Keine kommenden Treffer in geladenen Daten.")
            else:
                st.caption("Keine Programmdaten geladen. Nutzen Sie zuerst die Suche.")

            st.divider()
