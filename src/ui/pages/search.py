"""Search page — main search interface."""

import re

import pytz
import streamlit as st
from datetime import datetime

from config.channels import ALL_CHANNELS
from config.settings import DISPLAY_TIMEZONE
from src.search.engine import search
from src.notifications.store import add_subscription


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
        with filter_col2:
            show_past = st.checkbox("Vergangene Sendungen anzeigen", key="show_past")

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
        # Filter out past occurrences unless checkbox is checked
        now = datetime.now(pytz.timezone(DISPLAY_TIMEZONE))
        if not st.session_state.get("show_past", False):
            filtered_results = []
            for r in results:
                start = r.get("start_time", "")
                if start:
                    try:
                        dt = datetime.fromisoformat(start).astimezone(pytz.timezone(DISPLAY_TIMEZONE))
                        if dt >= now:
                            filtered_results.append(r)
                    except (ValueError, TypeError):
                        filtered_results.append(r)
                else:
                    filtered_results.append(r)
            display_results = filtered_results
        else:
            display_results = results

        st.subheader(f'Ergebnisse für "{last_query}" ({len(display_results)} Treffer)')

        if not display_results:
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
            for r in display_results:
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

            # Coverage per sender based on search results
            coverage = {}
            for r in display_results:
                channel = r.get("channel", "")
                end = r.get("end_time", "") or r.get("start_time", "")
                if not channel or not end:
                    continue
                try:
                    dt = datetime.fromisoformat(end).astimezone(berlin)
                    if channel not in coverage or dt > coverage[channel]:
                        coverage[channel] = dt
                except (ValueError, TypeError):
                    continue

            if coverage:
                st.subheader("Abdeckung pro Sender")
                coverage_data = []
                for ch in sorted(coverage):
                    latest = coverage[ch]
                    delta = latest - now
                    hours = delta.total_seconds() / 3600
                    if hours < 0:
                        bis_text = "Keine zukuenftigen Daten"
                    elif hours < 24:
                        bis_text = f"{hours:.1f} Std."
                    else:
                        days = hours / 24
                        bis_text = f"{days:.1f} Tage"
                    coverage_data.append({
                        "Sender": ch,
                        "Daten bis": latest.strftime("%d.%m.%Y %H:%M"),
                        "Reichweite": bis_text,
                    })
                st.dataframe(coverage_data, use_container_width=True, hide_index=True)

            # Email notification for this search
            with st.expander("Per E-Mail benachrichtigen"):
                notify_email = st.text_input(
                    "E-Mail-Adresse",
                    placeholder="ihre.email@beispiel.de",
                    key="notify_email_search",
                )
                if st.button("Benachrichtigung einrichten", key="notify_btn_search"):
                    if notify_email and re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", notify_email):
                        add_subscription(notify_email.strip(), last_query, channel_filter if 'channel_filter' in dir() else None)
                        st.success(f"Sie werden per E-Mail benachrichtigt, wenn '{last_query}' im Programm erscheint.")
                    else:
                        st.error("Bitte geben Sie eine gueltige E-Mail-Adresse ein.")

    # EPG coverage table
    cached = st.session_state.get("cached_listings", [])
    if cached:
        berlin = pytz.timezone(DISPLAY_TIMEZONE)
        now = datetime.now(berlin)
        coverage = {}
        for listing in cached:
            channel = listing.get("channel", "")
            end = listing.get("end_time", "") or listing.get("start_time", "")
            if not channel or not end:
                continue
            try:
                dt = datetime.fromisoformat(end).astimezone(berlin)
                if channel not in coverage or dt > coverage[channel]:
                    coverage[channel] = dt
            except (ValueError, TypeError):
                continue

        if coverage:
            with st.expander("Programmabdeckung pro Sender"):
                coverage_data = []
                for ch in sorted(coverage):
                    latest = coverage[ch]
                    delta = latest - now
                    hours = delta.total_seconds() / 3600
                    if hours < 0:
                        bis_text = "Keine zukünftigen Daten"
                    elif hours < 1:
                        bis_text = f"{int(delta.total_seconds() / 60)} Min."
                    else:
                        bis_text = f"{hours:.1f} Std."
                    coverage_data.append({
                        "Sender": ch,
                        "Daten bis": latest.strftime("%d.%m.%Y %H:%M"),
                        "Reichweite": bis_text,
                    })
                st.dataframe(coverage_data, use_container_width=True, hide_index=True)
