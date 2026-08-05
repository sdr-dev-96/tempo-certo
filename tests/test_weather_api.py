"""Unit tests for the pure parsing helpers in tempo_certo.weather_api.

fetch_forecast() itself performs a live network call and is intentionally
left untested for now — these tests only cover the parsing of an
already-fetched Open-Meteo response, which needs no mocking.
"""

from datetime import datetime
from zoneinfo import ZoneInfo

from tempo_certo import config
from tempo_certo.weather_api import hours_today, sunrise_hour


def test_hours_today_filters_by_current_date():
    today_str = datetime.now(ZoneInfo(config.TIMEZONE)).date().isoformat()
    data = {
        "hourly": {
            "time": [f"{today_str}T00:00", f"{today_str}T13:00", "2000-01-01T05:00"],
            "temperature_2m": [10, 20, 99],
            "apparent_temperature": [9, 19, 98],
            "precipitation_probability": [0, 40, 100],
            "wind_speed_10m": [5, 15, 999],
            "uv_index": [0, 6, 0],
            "weathercode": [0, 61, 99],
        }
    }

    result = hours_today(data)

    assert result == [
        {"hour": 0, "temp": 10, "feels_like": 9, "rain_prob": 0, "wind": 5, "uv": 0, "code": 0},
        {"hour": 13, "temp": 20, "feels_like": 19, "rain_prob": 40, "wind": 15, "uv": 6, "code": 61},
    ]


def test_sunrise_hour_parses_iso_timestamp():
    data = {"daily": {"sunrise": ["2026-08-05T06:42"]}}
    assert sunrise_hour(data) == 6


def test_sunrise_hour_missing_returns_none():
    assert sunrise_hour({"daily": {}}) is None
    assert sunrise_hour({}) is None
