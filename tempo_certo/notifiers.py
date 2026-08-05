"""Sending the notification (Telegram, ntfy.sh, email)."""

import logging
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from zoneinfo import ZoneInfo

import requests

from . import config, i18n

logger = logging.getLogger(__name__)


def strip_markdown(text):
    """Drop the *bold* markers used for Telegram; plain-text channels don't render them."""
    return text.replace("*", "")


def send_telegram(message):
    url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendMessage"
    resp = requests.post(
        url,
        data={"chat_id": config.TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"},
        timeout=10,
    )
    resp.raise_for_status()


def send_ntfy(message):
    url = f"https://ntfy.sh/{config.NTFY_TOPIC}"
    requests.post(
        url,
        data=strip_markdown(message).encode("utf-8"),
        headers={"Title": "Tempo Certo", "Tags": "sunny,shirt"},
        timeout=10,
    )


def send_email(message):
    msg = MIMEText(strip_markdown(message))
    msg["Subject"] = "Tempo Certo — conseils du jour"
    msg["From"] = config.SMTP_FROM
    msg["To"] = config.SMTP_TO

    with smtplib.SMTP(config.SMTP_HOST, config.SMTP_PORT) as server:
        server.starttls()
        server.login(config.SMTP_USER, config.SMTP_PASSWORD)
        server.sendmail(config.SMTP_FROM, [config.SMTP_TO], msg.as_string())


NOTIFY_SENDERS = {
    "telegram": send_telegram,
    "ntfy": send_ntfy,
    "email": send_email,
}


def notify(message):
    """Send via NOTIFY_METHOD, falling back to FALLBACK_NOTIFY_METHODS in order on failure."""
    methods = [config.NOTIFY_METHOD, *config.FALLBACK_NOTIFY_METHODS]
    last_error = None
    for method in methods:
        sender = NOTIFY_SENDERS.get(method)
        if sender is None:
            last_error = ValueError(f"Unknown notification method: {method}")
            logger.warning("Notification via %s failed: %s", method, last_error)
            continue
        try:
            sender(message)
            return
        except Exception as e:
            last_error = e
            logger.warning("Notification via %s failed: %s", method, e)

    raise last_error


def send_error_email(error_text):
    """
    Send an error alert by email, independent of NOTIFY_METHOD.
    Uses the same SMTP_* settings as the optional email notification method,
    so it works even if the daily notification normally goes via Telegram/ntfy.
    Never raises: a failure here must not mask the original error.
    """
    if not config.ERROR_ALERT_EMAIL_ENABLED:
        return
    try:
        today_label = i18n.date_label(datetime.now(ZoneInfo(config.TIMEZONE)), lang="fr")
        msg = MIMEText(
            f"Tempo Certo a rencontré une erreur le {today_label} :\n\n{error_text}\n\n"
            f"Voir le log du jour dans {config.LOG_DIR}/ sur le VPS pour le détail complet."
        )
        msg["Subject"] = "⚠️ Tempo Certo — erreur"
        msg["From"] = config.SMTP_FROM
        msg["To"] = config.ERROR_ALERT_EMAIL_TO

        with smtplib.SMTP(config.SMTP_HOST, config.SMTP_PORT) as server:
            server.starttls()
            server.login(config.SMTP_USER, config.SMTP_PASSWORD)
            server.sendmail(config.SMTP_FROM, [config.ERROR_ALERT_EMAIL_TO], msg.as_string())
    except Exception as email_error:
        # Logged here rather than raised: a failure to send the alert must not mask the original error.
        logger.error("Failed to send error alert email: %s", email_error)
