"""Weather fetching (Open-Meteo, free, no API key)."""

from datetime import datetime
from zoneinfo import ZoneInfo

import requests

import config


def fetch_forecast():
    """Fetch today's hourly forecast for the configured location."""
    params = {
        "latitude": config.LATITUDE,
        "longitude": config.LONGITUDE,
        "hourly": "temperature_2m,apparent_temperature,precipitation_probability,"
                  "weathercode,wind_speed_10m,uv_index",
        "timezone": config.TIMEZONE,
        "forecast_days": 1,
    }
    resp = requests.get("https://api.open-meteo.com/v1/forecast", params=params, timeout=15)
    resp.raise_for_status()
    return resp.json()


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
