"""Search page — main search interface."""

import pytz
import streamlit as st
from datetime import datetime

from config.channels import ALL_CHANNELS
from config.settings import DISPLAY_TIMEZONE
from src.search.engine import search


def render_search_page():
    """Render the main search page."""
    st.header("Suche")

    # Search input
    col1, col2 = st.columns([4, 1])
    with col1:
        query = st.text_input(
            "Suchbegriff",
            placeholder="z.B. Tatort, James Bond, Krimi...",
            key="search_query",
        )
    with col2:
        st.write("")
        st.write("")
        search_clicked = st.button("Suchen", type="primary", use_container_width=True)

    # Filters
    with st.expander("Filter"):
        filter_col1, filter_col2 = st.columns(2)
        with filter_col1:
            channels = ["Alle Sender"] + sorted(ALL_CHANNELS)
            selected_channel = st.selectbox("Sender", channels, key="filter_channel")

    # Execute search
    if search_clicked and query:
        channel_filter = None if selected_channel == "Alle Sender" else selected_channel

        # Get cached listings from session (if MagentaTV was fetched)
        cached = st.session_state.get("cached_listings", [])

        with st.spinner("Suche läuft..."):
            results = search(
                query=query,
                listings=cached,
                channel=channel_filter,
                enrich_from_api=True,
            )

        # Record in session history
        history = st.session_state.get("search_history", [])
        history.insert(0, {"query": query, "count": len(results), "time": datetime.now().isoformat()})
        st.session_state["search_history"] = history[:50]

        # Store results
        st.session_state["last_results"] = results
        st.session_state["last_query"] = query

    # Display results
    results = st.session_state.get("last_results", [])
    last_query = st.session_state.get("last_query", "")

    if last_query:
        st.subheader(f'Ergebnisse für "{last_query}" ({len(results)} Treffer)')

        if not results:
            st.info("Keine Treffer gefunden. Versuchen Sie einen anderen Suchbegriff.")
        else:
            # Add to favorites button
            if st.button(f'Als Favorit merken: "{last_query}"', key="add_fav_from_search"):
                favs = st.session_state.get("favorites", [])
                if last_query not in favs:
                    favs.append(last_query)
                    st.session_state["favorites"] = favs
                    st.success(f'"{last_query}" wurde zu den Favoriten hinzugefügt.')
                else:
                    st.info(f'"{last_query}" ist bereits ein Favorit.')

            # Results table
            berlin = pytz.timezone(DISPLAY_TIMEZONE)
            table_data = []
            for r in results:
                start = r.get("start_time", "")
                date_str = ""
                time_str = ""
                if start:
                    try:
                        dt = datetime.fromisoformat(start)
                        dt_berlin = dt.astimezone(berlin)
                        date_str = dt_berlin.strftime("%d.%m.%Y")
                        time_str = dt_berlin.strftime("%H:%M")
                    except (ValueError, TypeError):
                        date_str = start[:10] if len(start) >= 10 else start

                table_data.append({
                    "Sender": r.get("channel", ""),
                    "Datum": date_str,
                    "Uhrzeit": time_str,
                    "Titel": r.get("title", ""),
                    "Beschreibung": (r.get("description", "") or "")[:100],
                    "Relevanz": f"{r.get('relevance', 0):.0f}%",
                    "Quelle": r.get("source", ""),
                })

            st.dataframe(
                table_data,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Beschreibung": st.column_config.TextColumn(width="large"),
                },
            )
