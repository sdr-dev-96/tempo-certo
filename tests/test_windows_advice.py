"""Unit tests for tempo_certo.windows_advice.analyze_windows (pure logic, no network)."""

from tempo_certo.windows_advice import analyze_windows


def test_empty_hours_returns_none():
    assert analyze_windows([]) is None


def test_hot_day_with_evening_reopen():
    hours = [
        {"hour": 6, "temp": 18, "wind": 5},
        {"hour": 10, "temp": 25, "wind": 5},
        {"hour": 13, "temp": 30, "wind": 5},
        {"hour": 14, "temp": 32, "wind": 5},  # day peak
        {"hour": 18, "temp": 26, "wind": 5},
        {"hour": 21, "temp": 23, "wind": 5},  # first hour back under INDOOR_COMFORT_TEMP_C
        {"hour": 22, "temp": 20, "wind": 5},
    ]

    result = analyze_windows(hours, sunrise_h=6)

    assert result["day_max_temp"] == 32
    assert result["max_temp_hour"] == 14
    assert result["is_hot"] is True
    assert result["hot_close_hour"] == 12  # 1h before crossing the hot threshold at 13h
    assert result["hot_reopen_hour"] == 21
    assert result["is_cold_windy"] is False
    assert result["cold_windy_start"] is None
    assert result["cold_windy_end"] is None


def test_hot_day_without_evening_reopen():
    hours = [
        {"hour": 6, "temp": 20, "wind": 5},
        {"hour": 13, "temp": 30, "wind": 5},
        {"hour": 14, "temp": 33, "wind": 5},
        {"hour": 20, "temp": 27, "wind": 5},  # still above INDOOR_COMFORT_TEMP_C
    ]

    result = analyze_windows(hours, sunrise_h=6)

    assert result["is_hot"] is True
    assert result["hot_reopen_hour"] is None


def test_cold_and_windy_window():
    hours = [
        {"hour": 10, "temp": 15, "wind": 5},
        {"hour": 20, "temp": 8, "wind": 35},
        {"hour": 21, "temp": 7, "wind": 32},
        {"hour": 22, "temp": 9, "wind": 40},
    ]

    result = analyze_windows(hours, sunrise_h=7)

    assert result["is_hot"] is False
    assert result["is_cold_windy"] is True
    assert result["cold_windy_start"] == 20
    assert result["cold_windy_end"] == 22


def test_mild_day_has_no_advice():
    hours = [
        {"hour": 8, "temp": 15, "wind": 10},
        {"hour": 14, "temp": 22, "wind": 15},
        {"hour": 20, "temp": 17, "wind": 8},
    ]

    result = analyze_windows(hours, sunrise_h=7)

    assert result["is_hot"] is False
    assert result["hot_close_hour"] is None
    assert result["hot_reopen_hour"] is None
    assert result["is_cold_windy"] is False
    assert result["cold_windy_start"] is None
    assert result["cold_windy_end"] is None
