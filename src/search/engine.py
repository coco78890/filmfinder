"""Fuzzy search engine — stateless, works directly with API results."""

import logging
import re

from rapidfuzz import fuzz

from config.settings import FUZZY_SEARCH_THRESHOLD, FUZZY_WEIGHTS
from src.scrapers.mediathekview import fetch_mediathekview_listings

logger = logging.getLogger(__name__)

# German umlaut mapping
UMLAUT_MAP = {
    "ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss",
    "Ä": "Ae", "Ö": "Oe", "Ü": "Ue",
}
UMLAUT_PATTERN = re.compile("|".join(re.escape(k) for k in UMLAUT_MAP))


def normalize_german(text: str) -> str:
    """Normalize German umlauts for comparison."""
    return UMLAUT_PATTERN.sub(lambda m: UMLAUT_MAP[m.group()], text).lower().strip()


def compute_score(query: str, candidate: str) -> float:
    """Compute multi-strategy fuzzy match score (0-100)."""
    q = normalize_german(query)
    c = normalize_german(candidate)
    return round(
        FUZZY_WEIGHTS["ratio"] * fuzz.ratio(q, c)
        + FUZZY_WEIGHTS["partial_ratio"] * fuzz.partial_ratio(q, c)
        + FUZZY_WEIGHTS["token_sort_ratio"] * fuzz.token_sort_ratio(q, c)
        + FUZZY_WEIGHTS["token_set_ratio"] * fuzz.token_set_ratio(q, c),
        1,
    )


def search(
    query: str,
    listings: list[dict],
    channel: str | None = None,
    threshold: float = FUZZY_SEARCH_THRESHOLD,
    enrich_from_api: bool = True,
) -> list[dict]:
    """Search listings with fuzzy matching.

    Args:
        query: Search text.
        listings: Existing listings to search through (e.g. cached MagentaTV data).
        channel: Optional channel filter.
        threshold: Minimum fuzzy score.
        enrich_from_api: Also fetch from MediathekViewWeb live.

    Returns:
        Scored and sorted list of listing dicts with 'relevance' field.
    """
    if not query or not query.strip():
        return []

    query = query.strip()
    all_listings = list(listings)

    # Enrich with live MediathekViewWeb results
    if enrich_from_api:
        try:
            live = fetch_mediathekview_listings(query=query, size=30)
            # Deduplicate by (channel, title, start_time)
            existing = {(l["channel"], l["title"], l["start_time"]) for l in all_listings}
            for item in live:
                key = (item["channel"], item["title"], item["start_time"])
                if key not in existing:
                    all_listings.append(item)
                    existing.add(key)
        except Exception as e:
            logger.warning(f"Live API enrichment failed: {e}")

    # Filter by channel
    if channel:
        all_listings = [l for l in all_listings if l.get("channel") == channel]

    # Score candidates
    scored = []
    for listing in all_listings:
        title = listing.get("title", "")
        title_score = compute_score(query, title)

        desc = listing.get("description", "")
        desc_score = compute_score(query, desc) if desc else 0.0

        # Use the best of: title alone, or a blend that gives description real weight
        score = max(title_score, title_score * 0.6 + desc_score * 0.4)

        if score >= threshold:
            listing["relevance"] = score
            scored.append(listing)

    # Sort by relevance desc, then start_time asc
    scored.sort(key=lambda x: (-x["relevance"], x.get("start_time", "")))
    return scored
