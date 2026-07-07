"""
Tempo Certo configuration.
Adjust the values below to match your home, work schedule, and preferences.
"""

# ---------------------------------------------------------------------------
# Location (default: La Queue-en-Brie — adjust if needed)
# Find your coordinates at https://www.latlong.net/
# ---------------------------------------------------------------------------
LATITUDE = 48.7919594
LONGITUDE = 2.5722845
TIMEZONE = "Europe/Paris"

# ---------------------------------------------------------------------------
# Shutters / windows logic — HOT weather
# ---------------------------------------------------------------------------

# Temperature (°C) above which closing the shutters/windows is recommended
HOT_THRESHOLD_C = 26

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
# Work schedule (used for commute-specific clothing advice)
# Monday = 0 ... Sunday = 6. Value: "office" (Paris office), "remote"
# (télétravail), or "off". Adjust to match your actual weekly pattern.
# ---------------------------------------------------------------------------
WORK_MODE_BY_WEEKDAY = {
    0: "office",  # Monday
    1: "office",  # Tuesday
    2: "remote",  # Wednesday
    3: "office",  # Thursday
    4: "remote",  # Friday
    5: "off",     # Saturday
    6: "off",     # Sunday
}

# Approximate hours of your commute, used to check rain/wind/cold specifically
# at those times (waiting for public transport matters more than the daily average)
COMMUTE_MORNING_HOUR = 8   # leaving home
COMMUTE_EVENING_HOUR = 18  # heading back home

# ---------------------------------------------------------------------------
# Notification
# ---------------------------------------------------------------------------

# "telegram" (recommended), "ntfy" (free, no account), or "email" (SMTP)
NOTIFY_METHOD = "telegram"

# --- Telegram ---
# 1. Talk to @BotFather on Telegram, send /newbot, follow the steps to get a token
# 2. Send any message to your new bot, then open in a browser:
#    https://api.telegram.org/bot<TOKEN>/getUpdates
#    and copy the "chat":{"id": ...} value below
TELEGRAM_BOT_TOKEN = "CHANGE-ME:your-bot-token"
TELEGRAM_CHAT_ID = "CHANGE-ME"

# --- ntfy.sh (alternative) ---
# Pick a unique, hard-to-guess topic name (e.g. "tempo-certo-a8f3k2") and
# install the ntfy app (iOS/Android) or subscribe via https://ntfy.sh/<topic>
NTFY_TOPIC = "tempo-certo-CHANGE-ME"

# --- Email (SMTP), only used if NOTIFY_METHOD = "email" ---
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "your.address@gmail.com"
SMTP_PASSWORD = "app-password"  # use an "app password", not your main password
SMTP_FROM = "your.address@gmail.com"
SMTP_TO = "your.address@gmail.com"
