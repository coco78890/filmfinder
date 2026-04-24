"""FilmFinder — German TV Program Search App (stateless version)."""

import logging
import threading
import streamlit as st

st.set_page_config(
    page_title="FilmFinder",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

from src.ui.theme import inject_theme
inject_theme()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


@st.cache_resource(ttl=86400)
def _run_daily_notification_check():
    """Run notification check once per day in a background thread."""
    from config.settings import get_secret
    if not get_secret("SUPABASE_URL"):
        logger.info("Skipping notification check — SUPABASE_URL not configured.")
        return False

    def _check():
        try:
            from check_notifications import check_and_notify
            logger.info("Starting daily notification check...")
            check_and_notify()
            logger.info("Daily notification check completed.")
        except Exception as e:
            logger.error(f"Daily notification check failed: {e}")

    thread = threading.Thread(target=_check, daemon=True)
    thread.start()
    return True


# Trigger daily check in background (non-blocking)
_run_daily_notification_check()

# Hide the sidebar completely
st.markdown(
    "<style>[data-testid='stSidebar']{display:none}</style>",
    unsafe_allow_html=True,
)

from src.ui.pages.search import render_search_page
from src.ui.pages.notifications import render_notifications_page

tab_search, tab_notifications = st.tabs(["Suche", "Benachrichtigungen"])

with tab_search:
    render_search_page()

with tab_notifications:
    render_notifications_page()
