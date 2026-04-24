"""Daily embedding indexer — fetches TV listings and stores vector embeddings in Supabase.

Run periodically (e.g. via GitHub Actions cron) to keep the vector search index fresh.

Usage:
    python index_embeddings.py

Environment variables required:
    SUPABASE_URL  — Supabase project URL
    SUPABASE_KEY  — Supabase API key
"""

import logging

from config.settings import EMBEDDING_BROAD_QUERIES
from src.scrapers.mediathekview import fetch_mediathekview_listings
from src.search.vector import cleanup_old_embeddings, embed_batch, upsert_embeddings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def index_all():
    """Fetch listings from all sources, embed, and store in Supabase."""

    all_listings = []
    seen = set()

    def _add(listings):
        for item in listings:
            key = (item["channel"], item["title"], item.get("start_time", ""))
            if key not in seen:
                all_listings.append(item)
                seen.add(key)

    # 1. Fetch MagentaTV EPG (full schedule)
    try:
        from src.scrapers.magentatv import fetch_magentatv_listings
        magentatv = fetch_magentatv_listings()
        _add(magentatv)
        logger.info(f"MagentaTV: {len(magentatv)} listings fetched")
    except Exception as e:
        logger.warning(f"MagentaTV fetch failed: {e}")

    # 2. Fetch MediathekView with broad genre queries
    for query in EMBEDDING_BROAD_QUERIES:
        try:
            results = fetch_mediathekview_listings(query=query, size=50)
            before = len(all_listings)
            _add(results)
            added = len(all_listings) - before
            logger.info(f"MediathekView '{query}': {len(results)} fetched, {added} new")
        except Exception as e:
            logger.warning(f"MediathekView fetch failed for '{query}': {e}")

    if not all_listings:
        logger.warning("No listings fetched — nothing to index.")
        return

    logger.info(f"Total unique listings to embed: {len(all_listings)}")

    # 3. Build content texts for embedding
    texts = []
    for listing in all_listings:
        text = listing.get("title", "")
        desc = listing.get("description", "")
        if desc:
            text = f"{text}. {desc}"
        texts.append(text)

    # 4. Generate embeddings
    logger.info("Generating embeddings...")
    embeddings = embed_batch(texts)
    logger.info(f"Generated {len(embeddings)} embeddings")

    # 5. Upsert into Supabase
    logger.info("Upserting to Supabase...")
    count = upsert_embeddings(all_listings, embeddings)
    logger.info(f"Upserted {count} listings with embeddings")

    # 6. Clean up old entries
    try:
        deleted = cleanup_old_embeddings(days=7)
        logger.info(f"Cleaned up {deleted} old embeddings")
    except Exception as e:
        logger.warning(f"Cleanup failed: {e}")


if __name__ == "__main__":
    index_all()
