"""Notifications page — manage email alert subscriptions."""

import re

import streamlit as st

from config.channels import ALL_CHANNELS
from src.notifications.store import add_subscription


def _is_valid_email(email: str) -> bool:
    return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email))


def render_notifications_page():
    """Render the notifications management page."""
    st.header("Benachrichtigungen")
    st.caption("Lassen Sie sich per E-Mail benachrichtigen, wenn ein gewuenschter Film oder eine Sendung im Programm erscheint.")

    # Add new subscription
    with st.form("new_notification", clear_on_submit=True):
        st.subheader("Neue Benachrichtigung einrichten")
        email = st.text_input("E-Mail-Adresse", placeholder="ihre.email@beispiel.de")
        search_term = st.text_input("Suchbegriff", placeholder="z.B. Tatort, James Bond, Krimi...")
        channels = ["Alle Sender"] + sorted(ALL_CHANNELS)
        selected_channel = st.selectbox("Sender (optional)", channels)
        submitted = st.form_submit_button("Benachrichtigung erstellen", type="primary")

        if submitted:
            if not email or not _is_valid_email(email):
                st.error("Bitte geben Sie eine gueltige E-Mail-Adresse ein.")
            elif not search_term or not search_term.strip():
                st.error("Bitte geben Sie einen Suchbegriff ein.")
            else:
                channel_filter = None if selected_channel == "Alle Sender" else selected_channel
                try:
                    sub = add_subscription(email.strip(), search_term.strip(), channel_filter)
                    st.success(f"Benachrichtigung fuer '{search_term}' an {email} wurde eingerichtet!")
                except Exception as e:
                    st.error("Benachrichtigungen sind derzeit nicht verfuegbar. Bitte SUPABASE_URL und SUPABASE_KEY konfigurieren.")
