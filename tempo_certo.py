#!/usr/bin/env python3
"""
Tempo Certo
===========
Sends a daily Telegram notification with:
  1. Whether to close/reopen the shutters and windows, and when:
     - hot weather -> when to close (before peak heat) and reopen in the evening
     - cold + windy weather -> when to keep windows closed to avoid drafts/heat loss
  2. What to wear given the day's weather

Uses the free Open-Meteo API (no API key required).
Notification sent via Telegram by default. ntfy.sh and email (SMTP) are
available as alternatives — see config.py.

Meant to run via cron:
  0 6 * * 1-5    -> 6:00 AM on weekdays
  30 7 * * 6,0   -> 7:30 AM on weekends
"""

import sys

import requests

import config
from clothing_advice import analyze_clothing
from log_setup import setup_logging
from message_builder import build_message
from notifiers import notify
from weather_api import fetch_forecast, hours_today
from windows_advice import analyze_windows

logger = setup_logging()


def validate_credentials():
    """Make sure the credentials required by config.NOTIFY_METHOD were actually filled in."""
    if config.NOTIFY_METHOD == "telegram":
        if "CHANGE-ME" in config.TELEGRAM_BOT_TOKEN or "CHANGE-ME" in config.TELEGRAM_CHAT_ID:
            logger.error("TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID not configured — fill them in .env.")
            sys.exit(1)
    elif config.NOTIFY_METHOD == "ntfy":
        if "CHANGE-ME" in config.NTFY_TOPIC:
            logger.error("NTFY_TOPIC not configured — fill it in .env.")
            sys.exit(1)
    elif config.NOTIFY_METHOD == "email":
        if "CHANGE-ME" in config.SMTP_USER or "CHANGE-ME" in config.SMTP_PASSWORD:
            logger.error("SMTP_USER / SMTP_PASSWORD not configured — fill them in .env.")
            sys.exit(1)


def main():
    try:
        validate_credentials()
        data = fetch_forecast()
        hours = hours_today(data)
        if not hours:
            logger.error("No hourly data available for today.")
            sys.exit(1)

        windows = analyze_windows(hours)
        clothing = analyze_clothing(hours)
        message = build_message(windows, clothing)

        print(message)  # useful for cron logs

        if config.DRY_RUN:
            logger.info("DRY_RUN=1: notification not sent.")
        else:
            notify(message)

    except requests.RequestException as e:
        logger.error("Network error while calling the weather API or notification service: %s", e)
        sys.exit(1)
    except Exception as e:
        logger.error("Unexpected error: %s", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
