"""Clothing advice logic."""

from message_builder import WEATHER_CODE_LABELS


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

    return {
        "day_min_temp": day_min,
        "day_max_temp": day_max,
        "feels_max": feels_max,
        "max_rain_prob": max_rain_prob,
        "max_wind": max_wind,
        "max_uv": max_uv,
        "sky": WEATHER_CODE_LABELS.get(dominant_code, "temps variable"),
        "advice": advice,
    }
