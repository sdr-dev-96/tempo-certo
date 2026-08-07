"""
Tempo Certo configuration.
Adjust the values below to match your home, work schedule, and preferences.
"""

import os

from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# Location (default: Chennevières-sur-Marne — adjust if needed)
# Find your coordinates at https://www.latlong.net/
# ---------------------------------------------------------------------------
LATITUDE = 48.799549
LONGITUDE = 2.540125
TIMEZONE = "Europe/Paris"

# ---------------------------------------------------------------------------
# Shutters / windows logic — HOT weather
# ---------------------------------------------------------------------------

# Temperature (°C) above which closing the shutters/windows is recommended
HOT_THRESHOLD_C = 30

# Temperature (°C) below which it's considered safe to reopen in the evening
INDOOR_COMFORT_TEMP_C = 24

# Time window during which direct sun hits the apartment
# (per the apartment's layout: surrounded by greenery, direct sun only in
# the late afternoon / early evening)
SUN_EXPOSURE_START_HOUR = 16  # 4 PM
SUN_EXPOSURE_END_HOUR = 20    # 8 PM

# ---------------------------------------------------------------------------
# Shutters / windows logic — COLD + WINDY weather
# ---------------------------------------------------------------------------

# Temperature (°C) at or below which it's considered "cold"
COLD_THRESHOLD_C = 10

# Wind speed (km/h) at or above which it's considered "windy"
WINDY_THRESHOLD_KMH = 30

# ---------------------------------------------------------------------------
# Notification
# ---------------------------------------------------------------------------

# Language of the notification message: "fr" (default) or "en"
LANGUAGE = os.environ.get("LANGUAGE", "fr")

# Whether to prefix the notification with a greeting (e.g. "Bonjour !")
GREETING_ENABLED = os.environ.get("GREETING_ENABLED", "true").lower() == "true"

# First name used to personalize the notification's opening line (e.g. "Stéfane")
USER_FIRST_NAME = os.environ.get("USER_FIRST_NAME", "")

# Date format used in the notification, Python strftime syntax
DATE_FORMAT = os.environ.get("DATE_FORMAT", "%d/%m/%Y")

# "telegram" (recommended), "ntfy" (free, no account), or "email" (SMTP)
NOTIFY_METHOD = "telegram"

# Methods to try, in order, if NOTIFY_METHOD fails to send (e.g. ["ntfy"])
FALLBACK_NOTIFY_METHODS = []

# --- Telegram ---
# 1. Talk to @BotFather on Telegram, send /newbot, follow the steps to get a token
# 2. Send any message to your new bot, then open in a browser:
#    https://api.telegram.org/bot<TOKEN>/getUpdates
#    and copy the "chat":{"id": ...} value below
# Secrets live in .env (gitignored) — see .env.example for the template.
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "CHANGE-ME:your-bot-token")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "CHANGE-ME")

# --- ntfy.sh (alternative) ---
# Pick a unique, hard-to-guess topic name (e.g. "tempo-certo-a8f3k2") and
# install the ntfy app (iOS/Android) or subscribe via https://ntfy.sh/<topic>
NTFY_TOPIC = os.environ.get("NTFY_TOPIC", "tempo-certo-CHANGE-ME")

# --- Email (SMTP), used if NOTIFY_METHOD = "email" AND/OR for error alerts below ---
SMTP_HOST = os.environ.get("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
SMTP_USER = os.environ.get("SMTP_USER", "your.address@gmail.com")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD", "app-password")  # use an "app password", not your main password
SMTP_FROM = os.environ.get("SMTP_FROM", "your.address@gmail.com")
SMTP_TO = os.environ.get("SMTP_TO", "your.address@gmail.com")

# ---------------------------------------------------------------------------
# Logging — one file per day, kept in LOG_DIR, auto-cleaned after
# LOG_RETENTION_DAYS days
# ---------------------------------------------------------------------------
LOG_DIR = os.environ.get("LOG_DIR", "logs")
LOG_RETENTION_DAYS = int(os.environ.get("LOG_RETENTION_DAYS", "30"))

# ---------------------------------------------------------------------------
# Error alerting by email — independent of NOTIFY_METHOD, so you get an
# email even when the daily notification itself goes out via Telegram/ntfy.
# Reuses the SMTP_* credentials above (SMTP_HOST/USER/PASSWORD must be set
# for this to work, even if NOTIFY_METHOD is not "email").
# ---------------------------------------------------------------------------
ERROR_ALERT_EMAIL_ENABLED = os.environ.get("ERROR_ALERT_EMAIL_ENABLED", "true").lower() == "true"
ERROR_ALERT_EMAIL_TO = os.environ.get("ERROR_ALERT_EMAIL_TO", SMTP_TO)

# ---------------------------------------------------------------------------
# Run report by email — a short English summary sent after every run
# (success or failure), independent of NOTIFY_METHOD. Reuses the SMTP_*
# credentials above.
# ---------------------------------------------------------------------------
REPORT_EMAIL_ENABLED = os.environ.get("REPORT_EMAIL_ENABLED", "true").lower() == "true"
REPORT_EMAIL_TO = os.environ.get("REPORT_EMAIL_TO", SMTP_TO)

# ---------------------------------------------------------------------------
# Testing
# ---------------------------------------------------------------------------

# Set DRY_RUN=1 to print the message without sending a notification
DRY_RUN = os.environ.get("DRY_RUN", "0") == "1"
