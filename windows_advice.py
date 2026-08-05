"""Shutters / windows logic."""

import config


def analyze_windows(hours):
    """
    Determine what to do with shutters/windows today. Two independent
    scenarios can both apply on the same day:

    HOT scenario:
    - Find the hour of peak temperature.
    - Recommend closing 1h BEFORE the outdoor temperature crosses the "hot"
      threshold (config.HOT_THRESHOLD_C), to keep overnight coolness inside.
    - Never close later than the start of direct sun exposure
      (config.SUN_EXPOSURE_START_HOUR), since the apartment only gets direct
      sun in the late afternoon/evening.
    - Reopen in the evening once temperature drops back below
      config.INDOOR_COMFORT_TEMP_C.

    COLD + WINDY scenario:
    - Any hour where temperature <= config.COLD_THRESHOLD_C AND wind speed
      >= config.WINDY_THRESHOLD_KMH triggers a "keep windows closed" window,
      to avoid drafts and heat loss. Reports the start/end of that window.
    """
    if not hours:
        return None

    max_temp_hour = max(hours, key=lambda h: h["temp"])
    day_max = max_temp_hour["temp"]

    # --- Hot scenario ---
    hot_close_hour = None
    hot_reopen_hour = None
    is_hot = day_max >= config.HOT_THRESHOLD_C
    if is_hot:
        for h in hours:
            if h["temp"] >= config.HOT_THRESHOLD_C:
                hot_close_hour = max(h["hour"] - 1, 6)
                break
        if hot_close_hour is None:
            hot_close_hour = config.SUN_EXPOSURE_START_HOUR
        hot_close_hour = max(hot_close_hour, config.SUN_EXPOSURE_START_HOUR - 1)
        hot_close_hour = min(hot_close_hour, config.SUN_EXPOSURE_START_HOUR)

        afternoon_hours = [h for h in hours if h["hour"] >= max_temp_hour["hour"]]
        for h in afternoon_hours:
            if h["temp"] <= config.INDOOR_COMFORT_TEMP_C:
                hot_reopen_hour = h["hour"]
                break

    # --- Cold + windy scenario ---
    cold_windy_hours = [
        h["hour"] for h in hours
        if h["temp"] <= config.COLD_THRESHOLD_C and h["wind"] >= config.WINDY_THRESHOLD_KMH
    ]
    is_cold_windy = bool(cold_windy_hours)
    cold_windy_start = min(cold_windy_hours) if cold_windy_hours else None
    cold_windy_end = max(cold_windy_hours) if cold_windy_hours else None

    return {
        "day_max_temp": day_max,
        "max_temp_hour": max_temp_hour["hour"],
        "is_hot": is_hot,
        "hot_close_hour": hot_close_hour,
        "hot_reopen_hour": hot_reopen_hour,
        "is_cold_windy": is_cold_windy,
        "cold_windy_start": cold_windy_start,
        "cold_windy_end": cold_windy_end,
    }
