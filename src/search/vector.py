"""Vector search module — sentence-transformers + Supabase pgvector."""

import logging
import time
from datetime import datetime, timezone

import requests as http_requests
from requests.exceptions import RequestException

from config.settings import (
    EMBEDDING_TABLE,
    REQUEST_TIMEOUT,
    VECTOR_EMBEDDING_DIM,
    VECTOR_MODEL_NAME,
    VECTOR_SEARCH_COUNT,
    VECTOR_SEARCH_THRESHOLD,
    get_secret,
    get_supabase_key,
)

logger = logging.getLogger(__name__)

_model = None
UPSERT_CHUNK_SIZE = 50
SUPABASE_WRITE_RETRIES = 3


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
    if not get_secret("SUPABASE_URL") or not get_supabase_key():
        return False
    return _load_model() is not None


def _headers() -> dict:
    key = get_supabase_key()
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
    headers["Prefer"] = "resolution=merge-duplicates,return=minimal"

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

    # Keep request/response bodies modest; GitHub Actions can see chunked response drops
    # when Supabase returns rows with full embedding vectors.
    upserted = 0
    params = {"on_conflict": "channel,title,start_time"}
    for i in range(0, len(rows), UPSERT_CHUNK_SIZE):
        chunk = rows[i : i + UPSERT_CHUNK_SIZE]
        resp = _request_with_retries(
            "post",
            url,
            headers=headers,
            params=params,
            json=chunk,
            timeout=REQUEST_TIMEOUT,
        )
        resp.raise_for_status()
        upserted += len(chunk)

    return upserted


def _request_with_retries(method: str, url: str, **kwargs) -> http_requests.Response:
    """Run a Supabase write request with short backoff for transient transport errors."""
    last_error = None
    for attempt in range(1, SUPABASE_WRITE_RETRIES + 1):
        try:
            return http_requests.request(method, url, **kwargs)
        except RequestException as exc:
            last_error = exc
            if attempt == SUPABASE_WRITE_RETRIES:
                break
            delay = 2 ** (attempt - 1)
            logger.warning(
                "Supabase %s failed on attempt %s/%s: %s; retrying in %ss",
                method.upper(),
                attempt,
                SUPABASE_WRITE_RETRIES,
                exc,
                delay,
            )
            time.sleep(delay)
    raise last_error


def cleanup_old_embeddings(days: int = 7) -> None:
    """Delete embeddings older than `days` days."""
    from datetime import timedelta
    cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
    url = f"{get_secret('SUPABASE_URL')}/rest/v1/{EMBEDDING_TABLE}"
    headers = _headers()
    headers["Prefer"] = "return=minimal"
    params = {"indexed_at": f"lt.{cutoff}"}
    resp = _request_with_retries("delete", url, headers=headers, params=params, timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()
