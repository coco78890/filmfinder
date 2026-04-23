"""MagentaTV EPG API client — stateless, fetches live on each call."""

import logging
import time
from datetime import datetime, timedelta, timezone

import requests

from config.channels import normalize_channel_name
from config.settings import (
    MAGENTATV_AUTH_ENDPOINT,
    MAGENTATV_BASE_URL,
    MAGENTATV_CHANNELS_ENDPOINT,
    MAGENTATV_EPG_WINDOW_HOURS,
    MAGENTATV_PLAYBILL_ENDPOINT,
    MAGENTATV_REQUEST_DELAY,
    REQUEST_TIMEOUT,
)

logger = logging.getLogger(__name__)


def _authenticate(session: requests.Session) -> str | None:
    """Authenticate and return CSRF token, or None on failure."""
    try:
        payload = {
            "terminalid": "00:00:00:00:00:00",
            "mac": "00:00:00:00:00:00",
            "terminaltype": "WEBTV",
            "utcEnable": 1,
            "timezone": "Europe/Berlin",
            "userType": 3,
            "terminalvendor": "Unknown",
            "preSharedKeyID": "PC01P00002",
            "cnonce": "ABCDEFabcdef0123",
        }
        resp = session.post(
            f"{MAGENTATV_BASE_URL}{MAGENTATV_AUTH_ENDPOINT}",
            json=payload,
            timeout=REQUEST_TIMEOUT,
        )
        resp.raise_for_status()
        data = resp.json()
        csrf = data.get("csrfToken", "")
        if csrf:
            session.headers["X_CSRFToken"] = csrf
        return csrf
    except Exception as e:
        logger.error(f"MagentaTV auth failed: {e}")
        return None


def _fetch_channels(session: requests.Session) -> dict[str, str]:
    """Fetch channel list. Returns {contentId: display_name}."""
    try:
        payload = {
            "properties": [
                {"name": "logicalChannel", "include": "/channellist/logicalChannel/contentId,/channellist/logicalChannel/name"}
            ],
            "metaDataVer": "Channel/1.1",
            "channelNamespace": "2",
            "filterlist": [{"key": "IsHide", "value": "-1"}],
            "returnSat498": 0,
        }
        resp = session.post(
            f"{MAGENTATV_BASE_URL}{MAGENTATV_CHANNELS_ENDPOINT}",
            json=payload,
            timeout=REQUEST_TIMEOUT,
        )
        resp.raise_for_status()
        data = resp.json()
        channel_map = {}
        for ch in data.get("channellist", []):
            cid = ch.get("contentId", "")
            name = ch.get("name", "")
            if cid and name:
                channel_map[cid] = normalize_channel_name(name)
        return channel_map
    except Exception as e:
        logger.error(f"MagentaTV channel fetch failed: {e}")
        return {}


def _parse_time(time_str: str) -> str:
    """Parse MagentaTV time (YYYYMMDDHHmmSS UTC) to ISO 8601."""
    if not time_str:
        return ""
    try:
        dt = datetime.strptime(time_str[:14], "%Y%m%d%H%M%S").replace(tzinfo=timezone.utc)
        return dt.isoformat()
    except (ValueError, IndexError):
        return time_str


def fetch_magentatv_listings() -> list[dict]:
    """Fetch all current EPG listings from MagentaTV. Returns normalized dicts."""
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json",
        "X_cDVR": "1",
    })

    csrf = _authenticate(session)
    if not csrf:
        return []

    channel_map = _fetch_channels(session)
    if not channel_map:
        return []

    now = datetime.now(timezone.utc)
    begin = now.strftime("%Y%m%d%H%M%S")
    end = (now + timedelta(hours=MAGENTATV_EPG_WINDOW_HOURS)).strftime("%Y%m%d%H%M%S")

    all_listings = []
    for content_id, channel_name in channel_map.items():
        try:
            payload = {
                "channelid": content_id,
                "type": 2,
                "offset": 0,
                "count": -1,
                "isFill498": 1,
                "properties": [
                    {"name": "playbill", "include": "name,starttime,endtime,shortdesc,genre,id,cast,director"}
                ],
                "begintime": begin,
                "endtime": end,
            }
            resp = session.post(
                f"{MAGENTATV_BASE_URL}{MAGENTATV_PLAYBILL_ENDPOINT}",
                json=payload,
                timeout=REQUEST_TIMEOUT,
            )
            resp.raise_for_status()
            for item in resp.json().get("playbilllist", []):
                title = item.get("name", "").strip()
                if not title:
                    continue
                all_listings.append({
                    "channel": channel_name,
                    "title": title,
                    "description": item.get("shortdesc", "").strip(),
                    "start_time": _parse_time(item.get("starttime", "")),
                    "end_time": _parse_time(item.get("endtime", "")),
                    "genre": item.get("genre", "").strip(),
                    "source": "magentatv",
                })
        except Exception as e:
            logger.error(f"Playbill fetch failed for {channel_name}: {e}")
        time.sleep(MAGENTATV_REQUEST_DELAY)

    logger.info(f"MagentaTV: fetched {len(all_listings)} listings")
    return all_listings
