"""Clothing advice logic."""

from . import i18n
from .i18n import t


def analyze_clothing(hours):
    """Build clothing advice from the day's weather."""
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

    return {
        "day_min_temp": day_min,
        "day_max_temp": day_max,
        "feels_max": feels_max,
        "max_rain_prob": max_rain_prob,
        "max_wind": max_wind,
        "max_uv": max_uv,
        "sky": i18n.weather_label(dominant_code),
        "advice": advice,
    }
