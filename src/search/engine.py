"""Fuzzy search engine — stateless, works directly with API results."""

import logging
import re

from rapidfuzz import fuzz

from config.channels import ALL_CHANNELS
from config.settings import (
    FUZZY_SEARCH_THRESHOLD,
    FUZZY_WEIGHTS,
    FUZZY_WEIGHT,
    VECTOR_WEIGHT,
    VECTOR_ONLY_PENALTY,
)
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

    # Vector search enrichment
    try:
        from src.search.vector import is_available, vector_search as vs
        if is_available():
            known_channels = set(ALL_CHANNELS)
            vector_results = [vr for vr in vs(query) if vr.get("channel") in known_channels]
            if vector_results:
                fuzzy_by_key = {}
                for item in scored:
                    key = (item["channel"], item["title"], item.get("start_time", ""))
                    fuzzy_by_key[key] = item

                for vr in vector_results:
                    key = (vr["channel"], vr["title"], vr.get("start_time", ""))
                    similarity_pct = vr["similarity"] * 100

                    if key in fuzzy_by_key:
                        # Blend fuzzy + vector scores
                        existing = fuzzy_by_key[key]
                        existing["relevance"] = round(
                            FUZZY_WEIGHT * existing["relevance"] + VECTOR_WEIGHT * similarity_pct, 1
                        )
                    else:
                        # Vector-only result
                        vr["relevance"] = round(similarity_pct * VECTOR_ONLY_PENALTY, 1)
                        if vr["relevance"] >= threshold:
                            scored.append(vr)
    except Exception as e:
        logger.warning(f"Vector search failed, using fuzzy only: {e}")

    # Sort by relevance desc, then start_time asc
    scored.sort(key=lambda x: (-x["relevance"], x.get("start_time", "")))
    return scored
