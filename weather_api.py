"""Weather fetching (Open-Meteo, free, no API key)."""

import logging
import time
from datetime import datetime
from zoneinfo import ZoneInfo

import requests

import config

logger = logging.getLogger(__name__)


def fetch_forecast(max_retries=3, backoff_seconds=5):
    """Fetch today's hourly forecast for the configured location.

    Open-Meteo occasionally returns transient 5xx errors (server-side load).
    Retry a few times with an increasing delay before giving up.
    """
    params = {
        "latitude": config.LATITUDE,
        "longitude": config.LONGITUDE,
        "hourly": "temperature_2m,apparent_temperature,precipitation_probability,"
                  "weathercode,wind_speed_10m,uv_index",
        "daily": "sunrise",
        "timezone": config.TIMEZONE,
        "forecast_days": 1,
    }
    last_error = None
    for attempt in range(1, max_retries + 1):
        try:
            resp = requests.get("https://api.open-meteo.com/v1/forecast", params=params, timeout=15)
            if resp.status_code >= 500:
                # Transient server-side error: worth retrying
                last_error = requests.HTTPError(
                    f"{resp.status_code} Server Error: {resp.reason} for url: {resp.url}"
                )
                logger.warning(
                    "Open-Meteo returned %s (attempt %s/%s)", resp.status_code, attempt, max_retries
                )
                if attempt < max_retries:
                    time.sleep(backoff_seconds * attempt)
                    continue
                resp.raise_for_status()
            resp.raise_for_status()
            return resp.json()
        except requests.ConnectionError as e:
            last_error = e
            logger.warning(
                "Connection error reaching Open-Meteo (attempt %s/%s): %s", attempt, max_retries, e
            )
            if attempt < max_retries:
                time.sleep(backoff_seconds * attempt)
                continue
            raise
    raise last_error


def hours_today(data):
    """Return a list of dicts {hour, temp, feels_like, rain_prob, wind, uv, code} for today."""
    hourly = data["hourly"]
    today_str = datetime.now(ZoneInfo(config.TIMEZONE)).date().isoformat()
    result = []
    for i, ts in enumerate(hourly["time"]):
        if ts.startswith(today_str):
            result.append({
                "hour": int(ts[11:13]),
                "temp": hourly["temperature_2m"][i],
                "feels_like": hourly["apparent_temperature"][i],
                "rain_prob": hourly["precipitation_probability"][i],
                "wind": hourly["wind_speed_10m"][i],
                "uv": hourly["uv_index"][i],
                "code": hourly["weathercode"][i],
            })
    return result


def sunrise_hour(data):
    """Return today's sunrise hour (0-23), or None if the API didn't return it."""
    sunrise_times = data.get("daily", {}).get("sunrise")
    if not sunrise_times:
        return None
    return int(sunrise_times[0][11:13])
