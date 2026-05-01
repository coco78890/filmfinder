"""Standalone script to check subscriptions and send email notifications.

Run periodically (e.g. via cron) to notify subscribers about matching TV listings.

Usage:
    python check_notifications.py

Environment variables required:
    FILMFINDER_SMTP_HOST     - SMTP server (default: smtp.gmail.com)
    FILMFINDER_SMTP_PORT     - SMTP port (default: 587)
    FILMFINDER_SMTP_USER     - SMTP username
    FILMFINDER_SMTP_PASSWORD - SMTP password
    FILMFINDER_SMTP_FROM     - Sender address (default: SMTP_USER)
"""

import logging
from datetime import datetime, timezone

from src.notifications.store import deactivate_subscription, list_subscriptions
from src.notifications.notify import send_notification
from src.search.engine import search

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def _future_only(results: list[dict]) -> list[dict]:
    """Keep only results whose start_time is now or later."""
    now = datetime.now(timezone.utc)
    upcoming = []
    for r in results:
        start = r.get("start_time", "")
        if not start:
            continue
        try:
            dt = datetime.fromisoformat(start)
        except (ValueError, TypeError):
            continue
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        if dt >= now:
            upcoming.append(r)
    return upcoming


def check_and_notify():
    """Check all active subscriptions and send notifications for matches."""
    subs = list_subscriptions()
    active = [s for s in subs if s.get("active", True)]

    if not active:
        logger.info("No active subscriptions.")
        return

    logger.info(f"Checking {len(active)} active subscriptions...")

    for sub in active:
        search_term = sub["search_term"]
        email = sub["email"]
        channel = sub.get("channel")

        try:
            results = search(
                query=search_term,
                listings=[],
                channel=channel,
                enrich_from_api=True,
            )

            upcoming = _future_only(results)

            if upcoming:
                logger.info(f"Found {len(upcoming)} upcoming matches for '{search_term}' -> {email}")
                send_notification(email, search_term, upcoming)
                deactivate_subscription(sub["id"])
                logger.info(f"Subscription {sub['id']} deactivated after first notification")
            elif results:
                logger.info(
                    f"Only past matches for '{search_term}' ({len(results)} total) — keeping subscription active"
                )
            else:
                logger.info(f"No matches for '{search_term}'")

        except Exception:
            logger.exception(f"Failed to process subscription {sub['id']}")


if __name__ == "__main__":
    check_and_notify()
