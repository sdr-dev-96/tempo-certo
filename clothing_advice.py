"""Clothing advice logic."""

from datetime import datetime
from zoneinfo import ZoneInfo

import config
from message_builder import WEATHER_CODE_LABELS


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
        advice.append("Tenue très légère (coton/lin), vêtements amples et clairs.")
    elif feels_max >= 25:
        advice.append("Tenue légère d'été, manches courtes.")
    elif feels_max >= 18:
        advice.append("Tenue légère, une petite veste peut suffire le soir.")
    elif feels_max >= 10:
        advice.append("Prévoir une veste ou un pull, quelques couches.")
    else:
        advice.append("Habillage chaud : manteau, couches superposées.")

    # Day/night temperature swing
    if (day_max - day_min) >= 10:
        advice.append(
            f"Écart de température important ({round(day_min)}°C à {round(day_max)}°C) : "
            f"prévoir une couche à enlever/ajouter dans la journée."
        )

    # Rain (general)
    if max_rain_prob >= 60:
        advice.append("Risque de pluie élevé : parapluie ou imperméable conseillé.")
    elif max_rain_prob >= 30:
        advice.append("Risque de pluie modéré : un parapluie de sécurité peut être utile.")

    # Wind (general)
    if max_wind >= 40:
        advice.append("Vent fort prévu : évitez les vêtements amples/parapluies fragiles.")
    elif max_wind >= 25:
        advice.append("Un peu de vent : une couche coupe-vent peut aider.")

    # UV
    if max_uv >= 8:
        advice.append("Indice UV très élevé : crème solaire, chapeau et lunettes de soleil indispensables.")
    elif max_uv >= 6:
        advice.append("Indice UV élevé : pensez à la protection solaire.")

    # --- Commute-specific advice (office days only) ---
    commute_advice = []
    if work_mode == "office":
        morning = hour_data(hours, config.COMMUTE_MORNING_HOUR)
        evening = hour_data(hours, config.COMMUTE_EVENING_HOUR)

        if morning:
            if morning["rain_prob"] >= 40:
                commute_advice.append(
                    f"Pluie probable au moment du trajet ({config.COMMUTE_MORNING_HOUR}h) : "
                    f"prends un parapluie pour le trajet/les transports."
                )
            if morning["feels_like"] <= 5:
                commute_advice.append(
                    f"Il fera frais sur le trajet du matin (ressenti {round(morning['feels_like'])}°C) : "
                    f"prévois une couche chaude pour l'attente sur le quai/l'arrêt."
                )
            if morning["wind"] >= config.WINDY_THRESHOLD_KMH:
                commute_advice.append("Vent soutenu le matin : une capuche ou un bonnet peut aider en extérieur.")

        if evening and evening["rain_prob"] >= 40:
            commute_advice.append(
                f"Pluie probable au retour ({config.COMMUTE_EVENING_HOUR}h) : garde le parapluie sur toi."
            )

    return {
        "day_min_temp": day_min,
        "day_max_temp": day_max,
        "feels_max": feels_max,
        "max_rain_prob": max_rain_prob,
        "max_wind": max_wind,
        "max_uv": max_uv,
        "sky": WEATHER_CODE_LABELS.get(dominant_code, "temps variable"),
        "advice": advice,
        "commute_advice": commute_advice,
    }
