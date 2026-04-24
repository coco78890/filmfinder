"""MediathekViewWeb API client — stateless, fetches live on each call."""

import logging
from datetime import datetime, timedelta, timezone

import requests

from config.channels import normalize_channel_name
from config.settings import MEDIATHEKVIEW_API_URL, MEDIATHEKVIEW_DEFAULT_SIZE, REQUEST_TIMEOUT

logger = logging.getLogger(__name__)


def _parse_results(data: dict) -> list[dict]:
    """Parse API response into normalized listing dicts."""
    listings = []
    for item in data.get("result", {}).get("results", []):
        title = item.get("title", "").strip()
        topic = item.get("topic", "").strip()
        if not title and not topic:
            continue

        display_title = f"{topic} - {title}" if topic and title and topic != title else (title or topic)
        channel = normalize_channel_name(item.get("channel", ""))

        timestamp = item.get("timestamp", 0)
        duration = item.get("duration", 0)
        start_time = ""
        end_time = ""
        if timestamp:
            start_dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
            start_time = start_dt.isoformat()
            if duration:
                end_time = (start_dt + timedelta(seconds=duration)).isoformat()

        listings.append({
            "channel": channel,
            "title": display_title,
            "description": item.get("description", "").strip(),
            "start_time": start_time,
            "end_time": end_time,
            "genre": "",
            "source": "mediathekview",
            "external_url": item.get("url_video", ""),
        })
    return listings


def fetch_mediathekview_listings(query: str = "", size: int = MEDIATHEKVIEW_DEFAULT_SIZE) -> list[dict]:
    """Fetch listings from MediathekViewWeb. Returns normalized dicts.

    Runs two queries — one on title/topic, one on description — and merges
    the results, since the API treats multiple query objects as AND.
    """
    q = query if query else "*"
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; FilmFinder/1.0)",
        "Content-Type": "text/plain",
    }
    base_payload = {
        "sortBy": "timestamp",
        "sortOrder": "desc",
        "future": True,
        "offset": 0,
        "size": size,
    }

    listings = []
    seen = set()

    for fields in [["title", "topic"], ["description"]]:
        try:
            payload = {**base_payload, "queries": [{"fields": fields, "query": q}]}
            resp = requests.post(
                MEDIATHEKVIEW_API_URL, json=payload, headers=headers, timeout=REQUEST_TIMEOUT,
            )
            resp.raise_for_status()
            for item in _parse_results(resp.json()):
                key = (item["channel"], item["title"], item["start_time"])
                if key not in seen:
                    listings.append(item)
                    seen.add(key)
        except Exception as e:
            logger.warning(f"MediathekViewWeb fetch failed for fields {fields}: {e}")

    logger.info(f"MediathekViewWeb: fetched {len(listings)} listings (query='{query}')")
    return listings
