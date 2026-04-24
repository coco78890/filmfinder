"""Subscription store — Supabase backend for email alerts."""

import logging
import uuid
from datetime import datetime, timezone

import requests

from config.settings import SUPABASE_URL, SUPABASE_KEY

logger = logging.getLogger(__name__)

TABLE = "subscriptions"


def _headers() -> dict:
    return {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation",
    }


def _api(path: str = "") -> str:
    return f"{SUPABASE_URL}/rest/v1/{TABLE}{path}"


def add_subscription(email: str, search_term: str, channel: str | None = None) -> dict:
    """Add a new notification subscription. Returns the created subscription."""
    # Check for duplicate
    params = {"email": f"eq.{email}", "search_term": f"eq.{search_term}"}
    if channel:
        params["channel"] = f"eq.{channel}"
    else:
        params["channel"] = "is.null"

    resp = requests.get(_api(), headers=_headers(), params=params)
    resp.raise_for_status()
    existing = resp.json()
    if existing:
        return existing[0]

    entry = {
        "id": str(uuid.uuid4()),
        "email": email,
        "search_term": search_term,
        "channel": channel,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "last_notified": None,
        "active": True,
    }
    resp = requests.post(_api(), headers=_headers(), json=entry)
    resp.raise_for_status()
    logger.info(f"Added subscription: {email} for '{search_term}'")
    return resp.json()[0]


def remove_subscription(sub_id: str) -> bool:
    """Remove a subscription by ID. Returns True if found and removed."""
    resp = requests.delete(
        _api(), headers=_headers(), params={"id": f"eq.{sub_id}"}
    )
    resp.raise_for_status()
    deleted = resp.json()
    return len(deleted) > 0


def list_subscriptions(email: str | None = None) -> list[dict]:
    """List all subscriptions, optionally filtered by email."""
    params = {}
    if email:
        params["email"] = f"eq.{email}"
    resp = requests.get(_api(), headers=_headers(), params=params)
    resp.raise_for_status()
    return resp.json()


def update_last_notified(sub_id: str):
    """Update the last_notified timestamp for a subscription."""
    resp = requests.patch(
        _api(),
        headers=_headers(),
        params={"id": f"eq.{sub_id}"},
        json={"last_notified": datetime.now(timezone.utc).isoformat()},
    )
    resp.raise_for_status()
