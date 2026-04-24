"""Email notification sender — checks subscriptions and sends alerts."""

import logging
import smtplib
from email.message import EmailMessage

from config.settings import (
    SMTP_FROM,
    SMTP_HOST,
    SMTP_PASSWORD,
    SMTP_PORT,
    SMTP_USER,
)

logger = logging.getLogger(__name__)


def _clean(text: str) -> str:
    """Replace non-breaking spaces and other problematic chars."""
    return text.replace("\xa0", " ") if text else ""


def send_notification(to_email: str, search_term: str, matches: list[dict]):
    """Send an email notification about found matches."""
    if not SMTP_USER or not SMTP_PASSWORD:
        logger.error("SMTP credentials not configured. Set FILMFINDER_SMTP_USER and FILMFINDER_SMTP_PASSWORD.")
        raise RuntimeError("SMTP-Zugangsdaten sind nicht konfiguriert.")

    search_term = _clean(search_term)

    msg = EmailMessage()
    msg["Subject"] = f"FilmFinder: Treffer fuer '{search_term}'"
    msg["From"] = SMTP_FROM
    msg["To"] = to_email

    # Build plain text body
    lines = [f"Hallo,\n\nfuer Ihren Suchbegriff '{search_term}' wurden {len(matches)} Treffer gefunden:\n"]
    for m in matches[:20]:
        channel = _clean(m.get("channel", ""))
        title = _clean(m.get("title", ""))
        start = m.get("start_time", "")
        date_str = start[:10] if len(start) >= 10 else start
        lines.append(f"  - {channel}: {title} ({date_str})")
    if len(matches) > 20:
        lines.append(f"\n  ... und {len(matches) - 20} weitere Treffer.")
    lines.append("\nViele Gruesse,\nIhr FilmFinder")
    text_body = "\n".join(lines)

    # Build HTML body
    rows = ""
    for m in matches[:20]:
        channel = _clean(m.get("channel", ""))
        title = _clean(m.get("title", ""))
        start = m.get("start_time", "")
        date_str = start[:10] if len(start) >= 10 else start
        desc = _clean((m.get("description", "") or "")[:80])
        rows += f"<tr><td>{channel}</td><td>{title}</td><td>{date_str}</td><td>{desc}</td></tr>\n"

    html_body = f"""\
<html>
<body>
<p>Hallo,</p>
<p>fuer Ihren Suchbegriff <strong>'{search_term}'</strong> wurden <strong>{len(matches)}</strong> Treffer gefunden:</p>
<table border="1" cellpadding="5" cellspacing="0" style="border-collapse:collapse;">
<tr><th>Sender</th><th>Titel</th><th>Datum</th><th>Beschreibung</th></tr>
{rows}
</table>
{"<p>... und " + str(len(matches) - 20) + " weitere Treffer.</p>" if len(matches) > 20 else ""}
<p>Viele Gruesse,<br>Ihr FilmFinder</p>
</body>
</html>"""

    msg.set_content(text_body)
    msg.add_alternative(html_body, subtype="html")

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)

    logger.info(f"Notification sent to {to_email} for '{search_term}' ({len(matches)} matches)")
