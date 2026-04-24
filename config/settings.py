"""Application settings and constants."""

# MagentaTV EPG API
MAGENTATV_BASE_URL = "https://api.prod.sngtv.magentatv.de"
MAGENTATV_AUTH_ENDPOINT = "/EPG/JSON/Authenticate"
MAGENTATV_CHANNELS_ENDPOINT = "/EPG/JSON/AllChannel"
MAGENTATV_PLAYBILL_ENDPOINT = "/EPG/JSON/PlayBillList"
MAGENTATV_REQUEST_DELAY = 1.0  # seconds between requests
MAGENTATV_EPG_WINDOW_HOURS = 48  # 2-day window

# MediathekViewWeb API
MEDIATHEKVIEW_API_URL = "https://mediathekviewweb.de/api/query"
MEDIATHEKVIEW_DEFAULT_SIZE = 50

# Request settings
REQUEST_TIMEOUT = 30  # seconds

# Search
FUZZY_SEARCH_THRESHOLD = 60
FUZZY_WEIGHTS = {
    "ratio": 0.15,
    "partial_ratio": 0.35,
    "token_sort_ratio": 0.2,
    "token_set_ratio": 0.3,
}

# Timezone
DISPLAY_TIMEZONE = "Europe/Berlin"

# Email / SMTP settings (configure via environment variables)
import os

SMTP_HOST = os.environ.get("FILMFINDER_SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("FILMFINDER_SMTP_PORT") or "587")
SMTP_USER = os.environ.get("FILMFINDER_SMTP_USER", "")
SMTP_PASSWORD = os.environ.get("FILMFINDER_SMTP_PASSWORD", "")
SMTP_FROM = os.environ.get("FILMFINDER_SMTP_FROM", SMTP_USER)

# Vector search (pgvector)
VECTOR_MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"
VECTOR_EMBEDDING_DIM = 384
VECTOR_SEARCH_THRESHOLD = 0.45  # minimum cosine similarity (0-1)
VECTOR_SEARCH_COUNT = 30
VECTOR_WEIGHT = 0.4   # weight of vector score in hybrid blend
FUZZY_WEIGHT = 0.6    # weight of fuzzy score in hybrid blend
VECTOR_ONLY_PENALTY = 0.7  # multiplier for vector-only results
EMBEDDING_TABLE = "listing_embeddings"
EMBEDDING_BROAD_QUERIES = [
    "Film", "Serie", "Dokumentation", "Nachrichten", "Sport",
    "Krimi", "Komoedie", "Show", "Magazin", "Thriller", "Drama",
]

# Supabase (subscription storage)
# Supports both env vars (GitHub Actions) and st.secrets (Streamlit Cloud)
def get_secret(key: str, default: str = "") -> str:
    """Read a secret from env vars first, then st.secrets."""
    val = os.environ.get(key, "")
    if val:
        return val
    try:
        import streamlit as st
        return st.secrets.get(key, default)
    except Exception:
        return default
