"""Unit tests for tempo_certo.clothing_advice.analyze_clothing (pure logic, no network)."""

from tempo_certo import i18n
from tempo_certo.clothing_advice import analyze_clothing


def test_empty_hours_returns_none():
    assert analyze_clothing([]) is None


def test_hot_summer_day():
    hours = [
        {"hour": 8, "temp": 22, "feels_like": 22, "rain_prob": 10, "wind": 10, "uv": 3, "code": 0},
        {"hour": 14, "temp": 32, "feels_like": 31, "rain_prob": 20, "wind": 15, "uv": 9, "code": 0},
        {"hour": 20, "temp": 24, "feels_like": 23, "rain_prob": 5, "wind": 5, "uv": 1, "code": 0},
    ]

    result = analyze_clothing(hours)

    assert result["day_min_temp"] == 22
    assert result["day_max_temp"] == 32
    assert result["feels_max"] == 31
    assert result["sky"] == i18n.weather_label(0)
    assert result["advice"] == [
        i18n.t("outfit_very_light"),
        i18n.t("temp_swing", min_temp=22, max_temp=32),
        i18n.t("uv_very_high"),
    ]


def test_cold_rainy_windy_day():
    hours = [
        {"hour": 8, "temp": 3, "feels_like": 2, "rain_prob": 50, "wind": 35, "uv": 1, "code": 61},
        {"hour": 14, "temp": 10, "feels_like": 9, "rain_prob": 30, "wind": 20, "uv": 2, "code": 61},
        {"hour": 18, "temp": 6, "feels_like": 5, "rain_prob": 60, "wind": 15, "uv": 0, "code": 61},
    ]

    result = analyze_clothing(hours)

    assert result["advice"] == [
        i18n.t("outfit_warm"),
        i18n.t("rain_high"),
        i18n.t("wind_light"),
    ]
