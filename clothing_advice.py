"""Clothing advice logic."""

from datetime import datetime
from zoneinfo import ZoneInfo

import config
import i18n
from i18n import t


def get_today_work_mode():
    """Return 'office', 'remote' or 'off' for today, based on config.WORK_MODE_BY_WEEKDAY."""
    weekday = datetime.now(ZoneInfo(config.TIMEZONE)).weekday()  # Monday = 0 ... Sunday = 6
    return config.WORK_MODE_BY_WEEKDAY.get(weekday, "off")


def hour_data(hours, target_hour):
    """Return the hour dict closest to target_hour, or None if hours is empty."""
    if not hours:
        return None
    return min(hours, key=lambda h: abs(h["hour"] - target_hour))


def analyze_clothing(hours, work_mode):
    """Build clothing advice from the day's weather, including commute notes."""
    if not hours:
        return None

    temps = [h["temp"] for h in hours]
    feels = [h["feels_like"] for h in hours]
    rain_probs = [h["rain_prob"] for h in hours]
    winds = [h["wind"] for h in hours]
    uvs = [h["uv"] for h in hours]

    day_min, day_max = min(temps), max(temps)
    feels_max = max(feels)
    max_rain_prob = max(rain_probs)
    max_wind = max(winds)
    max_uv = max(uvs)
    # Use the sky condition at the hottest hour rather than the day's most
    # frequent code, which is more representative of what the day "feels" like.
    dominant_code = max(hours, key=lambda h: h["temp"])["code"]

    advice = []

    # Base outfit according to max "feels like" temperature
    if feels_max >= 30:
        advice.append(t("outfit_very_light"))
    elif feels_max >= 25:
        advice.append(t("outfit_light_summer"))
    elif feels_max >= 18:
        advice.append(t("outfit_light_evening_jacket"))
    elif feels_max >= 10:
        advice.append(t("outfit_jacket_layers"))
    else:
        advice.append(t("outfit_warm"))

    # Day/night temperature swing
    if (day_max - day_min) >= 10:
        advice.append(t("temp_swing", min_temp=round(day_min), max_temp=round(day_max)))

    # Rain (general)
    if max_rain_prob >= 60:
        advice.append(t("rain_high"))
    elif max_rain_prob >= 30:
        advice.append(t("rain_moderate"))

    # Wind (general)
    if max_wind >= 40:
        advice.append(t("wind_strong"))
    elif max_wind >= 25:
        advice.append(t("wind_light"))

    # UV
    if max_uv >= 8:
        advice.append(t("uv_very_high"))
    elif max_uv >= 6:
        advice.append(t("uv_high"))

    # --- Commute-specific advice (office days only) ---
    commute_advice = []
    if work_mode == "office":
        morning = hour_data(hours, config.COMMUTE_MORNING_HOUR)
        evening = hour_data(hours, config.COMMUTE_EVENING_HOUR)

        if morning:
            if morning["rain_prob"] >= 40:
                commute_advice.append(t("commute_rain_morning", hour=config.COMMUTE_MORNING_HOUR))
            if morning["feels_like"] <= 5:
                commute_advice.append(
                    t("commute_cold_morning", feels=round(morning["feels_like"]))
                )
            if morning["wind"] >= config.WINDY_THRESHOLD_KMH:
                commute_advice.append(t("commute_wind_morning"))

        if evening and evening["rain_prob"] >= 40:
            commute_advice.append(t("commute_rain_evening", hour=config.COMMUTE_EVENING_HOUR))

    return {
        "day_min_temp": day_min,
        "day_max_temp": day_max,
        "feels_max": feels_max,
        "max_rain_prob": max_rain_prob,
        "max_wind": max_wind,
        "max_uv": max_uv,
        "sky": i18n.weather_label(dominant_code),
        "advice": advice,
        "commute_advice": commute_advice,
    }
