"""Vector search module — sentence-transformers + Supabase pgvector."""

import logging
from datetime import datetime, timezone

import requests as http_requests

from config.settings import (
    EMBEDDING_TABLE,
    REQUEST_TIMEOUT,
    VECTOR_EMBEDDING_DIM,
    VECTOR_MODEL_NAME,
    VECTOR_SEARCH_COUNT,
    VECTOR_SEARCH_THRESHOLD,
    get_secret,
)

logger = logging.getLogger(__name__)

_model = None


def _load_model():
    """Load the sentence-transformer model (singleton)."""
    global _model
    if _model is None:
        try:
            from sentence_transformers import SentenceTransformer
            _model = SentenceTransformer(VECTOR_MODEL_NAME)
            logger.info(f"Loaded embedding model: {VECTOR_MODEL_NAME}")
        except ImportError:
            logger.warning("sentence-transformers not installed — vector search disabled.")
    return _model


def is_available() -> bool:
    """Check if vector search is configured (model + Supabase)."""
    if not get_secret("SUPABASE_URL") or not get_secret("SUPABASE_KEY"):
        return False
    return _load_model() is not None


def _headers() -> dict:
    key = get_secret("SUPABASE_KEY")
    return {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "Prefer": "return=representation",
    }


def embed_text(text: str) -> list[float]:
    """Embed a single text string. Returns list of floats."""
    model = _load_model()
    if model is None:
        raise RuntimeError("Embedding model not available")
    return model.encode(text, normalize_embeddings=True).tolist()


def embed_batch(texts: list[str]) -> list[list[float]]:
    """Embed multiple texts efficiently. Returns list of float lists."""
    model = _load_model()
    if model is None:
        raise RuntimeError("Embedding model not available")
    embeddings = model.encode(texts, normalize_embeddings=True, batch_size=64, show_progress_bar=True)
    return [e.tolist() for e in embeddings]


def vector_search(
    query: str,
    match_count: int = VECTOR_SEARCH_COUNT,
    threshold: float = VECTOR_SEARCH_THRESHOLD,
) -> list[dict]:
    """Embed query and search Supabase pgvector. Returns listing dicts with 'similarity'."""
    query_embedding = embed_text(query)
    url = f"{get_secret('SUPABASE_URL')}/rest/v1/rpc/match_listings"
    payload = {
        "query_embedding": query_embedding,
        "match_threshold": threshold,
        "match_count": match_count,
    }
    resp = http_requests.post(url, headers=_headers(), json=payload, timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()
    return resp.json()


def upsert_embeddings(listings: list[dict], embeddings: list[list[float]]) -> int:
    """Upsert listing+embedding pairs into Supabase. Returns count of rows upserted."""
    url = f"{get_secret('SUPABASE_URL')}/rest/v1/{EMBEDDING_TABLE}"
    headers = _headers()
    headers["Prefer"] = "resolution=merge-duplicates,return=representation"

    rows = []
    for listing, embedding in zip(listings, embeddings):
        content_text = listing.get("title", "")
        desc = listing.get("description", "")
        if desc:
            content_text = f"{content_text}. {desc}"

        rows.append({
            "channel": listing.get("channel", ""),
            "title": listing.get("title", ""),
            "description": desc,
            "start_time": listing.get("start_time", ""),
            "end_time": listing.get("end_time", ""),
            "genre": listing.get("genre", ""),
            "source": listing.get("source", ""),
            "external_url": listing.get("external_url", ""),
            "content_text": content_text,
            "embedding": embedding,
            "indexed_at": datetime.now(timezone.utc).isoformat(),
        })

    # Upsert in chunks of 100
    upserted = 0
    for i in range(0, len(rows), 100):
        chunk = rows[i : i + 100]
        resp = http_requests.post(url, headers=headers, json=chunk, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        upserted += len(resp.json())

    return upserted


def cleanup_old_embeddings(days: int = 7) -> int:
    """Delete embeddings older than `days` days. Returns count deleted."""
    from datetime import timedelta
    cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
    url = f"{get_secret('SUPABASE_URL')}/rest/v1/{EMBEDDING_TABLE}"
    params = {"indexed_at": f"lt.{cutoff}"}
    resp = http_requests.delete(url, headers=_headers(), params=params, timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()
    deleted = resp.json()
    return len(deleted)
