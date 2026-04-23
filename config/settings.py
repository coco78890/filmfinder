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
