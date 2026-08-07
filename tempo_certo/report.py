"""Short English run report sent by email after every run, independent of NOTIFY_METHOD."""

import logging
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from zoneinfo import ZoneInfo

from . import config, i18n

logger = logging.getLogger(__name__)


def send_report_email(success: bool, detail: str):
    """
    Send a short English run report by email, independent of NOTIFY_METHOD.
    Uses the same SMTP_* credentials as the notification/error-alert emails.
    Never raises: a failure here must not crash the main run.
    """
    if not config.REPORT_EMAIL_ENABLED:
        return
    try:
        today_label = i18n.date_label(datetime.now(ZoneInfo(config.TIMEZONE)), lang="en")
        status = "SUCCESS" if success else "FAILURE"
        body = f"Tempo Certo run on {today_label}: {status}\n\n{detail}"

        msg = MIMEText(body)
        msg["Subject"] = f"Tempo Certo — run report ({status.lower()})"
        msg["From"] = config.SMTP_FROM
        msg["To"] = config.REPORT_EMAIL_TO

        with smtplib.SMTP(config.SMTP_HOST, config.SMTP_PORT) as server:
            server.starttls()
            server.login(config.SMTP_USER, config.SMTP_PASSWORD)
            server.sendmail(config.SMTP_FROM, [config.REPORT_EMAIL_TO], msg.as_string())
    except Exception as report_error:
        logger.error("Failed to send run report email: %s", report_error)
