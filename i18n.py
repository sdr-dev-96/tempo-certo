"""Translations for the daily notification message."""

import config

DEFAULT_LANGUAGE = "fr"

WEEKDAYS = {
    "fr": ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"],
    "en": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
}

MONTHS = {
    "fr": [
        "janvier", "février", "mars", "avril", "mai", "juin",
        "juillet", "août", "septembre", "octobre", "novembre", "décembre",
    ],
    "en": [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December",
    ],
}

WEATHER_CODE_LABELS = {
    "fr": {
        0: "ciel dégagé", 1: "plutôt dégagé", 2: "partiellement nuageux", 3: "couvert",
        45: "brouillard", 48: "brouillard givrant",
        51: "bruine légère", 53: "bruine", 55: "bruine forte",
        61: "pluie légère", 63: "pluie", 65: "pluie forte",
        71: "neige légère", 73: "neige", 75: "neige forte",
        80: "averses légères", 81: "averses", 82: "averses fortes",
        95: "orages", 96: "orages avec grêle", 99: "orages violents",
    },
    "en": {
        0: "clear sky", 1: "mostly clear", 2: "partly cloudy", 3: "overcast",
        45: "fog", 48: "freezing fog",
        51: "light drizzle", 53: "drizzle", 55: "heavy drizzle",
        61: "light rain", 63: "rain", 65: "heavy rain",
        71: "light snow", 73: "snow", 75: "heavy snow",
        80: "light showers", 81: "showers", 82: "heavy showers",
        95: "thunderstorm", 96: "thunderstorm with hail", 99: "severe thunderstorm",
    },
}

WEATHER_CODE_FALLBACK = {
    "fr": "temps variable",
    "en": "variable weather",
}

STRINGS = {
    "fr": {
        "header": "☀️ *Tempo Certo* — {date}",
        "windows_section_title": "*🪟 Volets / fenêtres*",
        "hot_close": "• Chaleur : fermer vers *{close_hour}h* (pic à *{max_temp}°C* vers {max_temp_hour}h)",
        "hot_reopen": "• Réouverture possible vers *{reopen_hour}h* en soirée",
        "hot_no_reopen": "• Garder fermé toute la soirée, la fraîcheur ne revient pas vite",
        "cold_windy": (
            "• Froid + vent : garder les fenêtres fermées entre *{start}h* "
            "et *{end}h* pour éviter les déperditions de chaleur"
        ),
        "no_window_advice": "• Rien de particulier aujourd'hui (max {max_temp}°C, peu de vent)",
        "clothing_section_title": "*👕 Tenue du jour*",
        "clothing_summary": "{sky}, {min_temp}°C → {max_temp}°C (ressenti max {feels_max}°C)",
        "commute_section_title": "*🚇 Trajet bureau (Paris)*",
        "remote_note": "🏠 Télétravail aujourd'hui — pas de contrainte de trajet",
        "outfit_very_light": "Tenue très légère (coton/lin), vêtements amples et clairs.",
        "outfit_light_summer": "Tenue légère d'été, manches courtes.",
        "outfit_light_evening_jacket": "Tenue légère, une petite veste peut suffire le soir.",
        "outfit_jacket_layers": "Prévoir une veste ou un pull, quelques couches.",
        "outfit_warm": "Habillage chaud : manteau, couches superposées.",
        "temp_swing": (
            "Écart de température important ({min_temp}°C à {max_temp}°C) : "
            "prévoir une couche à enlever/ajouter dans la journée."
        ),
        "rain_high": "Risque de pluie élevé : parapluie ou imperméable conseillé.",
        "rain_moderate": "Risque de pluie modéré : un parapluie de sécurité peut être utile.",
        "wind_strong": "Vent fort prévu : évitez les vêtements amples/parapluies fragiles.",
        "wind_light": "Un peu de vent : une couche coupe-vent peut aider.",
        "uv_very_high": "Indice UV très élevé : crème solaire, chapeau et lunettes de soleil indispensables.",
        "uv_high": "Indice UV élevé : pensez à la protection solaire.",
        "commute_rain_morning": (
            "Pluie probable au moment du trajet ({hour}h) : "
            "prends un parapluie pour le trajet/les transports."
        ),
        "commute_cold_morning": (
            "Il fera frais sur le trajet du matin (ressenti {feels}°C) : "
            "prévois une couche chaude pour l'attente sur le quai/l'arrêt."
        ),
        "commute_wind_morning": "Vent soutenu le matin : une capuche ou un bonnet peut aider en extérieur.",
        "commute_rain_evening": "Pluie probable au retour ({hour}h) : garde le parapluie sur toi.",
    },
    "en": {
        "header": "☀️ *Tempo Certo* — {date}",
        "windows_section_title": "*🪟 Shutters / windows*",
        "hot_close": "• Heat: close around *{close_hour}h* (peak of *{max_temp}°C* around {max_temp_hour}h)",
        "hot_reopen": "• Reopening possible around *{reopen_hour}h* in the evening",
        "hot_no_reopen": "• Keep everything closed all evening, it won't cool down quickly",
        "cold_windy": (
            "• Cold + wind: keep windows closed between *{start}h* "
            "and *{end}h* to avoid heat loss"
        ),
        "no_window_advice": "• Nothing special today (max {max_temp}°C, little wind)",
        "clothing_section_title": "*👕 Outfit of the day*",
        "clothing_summary": "{sky}, {min_temp}°C → {max_temp}°C (feels like up to {feels_max}°C)",
        "commute_section_title": "*🚇 Office commute (Paris)*",
        "remote_note": "🏠 Working from home today — no commute to worry about",
        "outfit_very_light": "Very light outfit (cotton/linen), loose and light-colored clothes.",
        "outfit_light_summer": "Light summer outfit, short sleeves.",
        "outfit_light_evening_jacket": "Light outfit, a light jacket may help in the evening.",
        "outfit_jacket_layers": "Bring a jacket or sweater, a few layers.",
        "outfit_warm": "Dress warmly: coat, layered clothing.",
        "temp_swing": (
            "Large temperature swing ({min_temp}°C to {max_temp}°C): "
            "plan a layer you can add/remove during the day."
        ),
        "rain_high": "High chance of rain: umbrella or raincoat recommended.",
        "rain_moderate": "Moderate chance of rain: a backup umbrella could help.",
        "wind_strong": "Strong wind expected: avoid loose clothing/flimsy umbrellas.",
        "wind_light": "A bit of wind: a windbreaker layer can help.",
        "uv_very_high": "Very high UV index: sunscreen, hat and sunglasses essential.",
        "uv_high": "High UV index: consider sun protection.",
        "commute_rain_morning": (
            "Rain likely during your commute ({hour}h): "
            "bring an umbrella for the trip/transit."
        ),
        "commute_cold_morning": (
            "It'll be chilly on the morning commute (feels like {feels}°C): "
            "plan a warm layer while waiting on the platform/stop."
        ),
        "commute_wind_morning": "Strong wind in the morning: a hood or beanie can help outdoors.",
        "commute_rain_evening": "Rain likely on the way back ({hour}h): keep the umbrella with you.",
    },
}


def _lang(lang=None):
    lang = lang or getattr(config, "LANGUAGE", DEFAULT_LANGUAGE)
    return lang if lang in STRINGS else DEFAULT_LANGUAGE


def t(key, lang=None, **kwargs):
    """Return the translated, formatted string for `key` in `lang` (default: config.LANGUAGE)."""
    lang = _lang(lang)
    template = STRINGS[lang].get(key, STRINGS[DEFAULT_LANGUAGE][key])
    return template.format(**kwargs) if kwargs else template


def date_label(dt, lang=None):
    """Format a date in the given language without depending on the system locale."""
    lang = _lang(lang)
    weekday = WEEKDAYS[lang][dt.weekday()]
    month = MONTHS[lang][dt.month - 1]
    return f"{weekday} {dt.day:02d} {month} {dt.year}"


def weather_label(code, lang=None):
    """Return the human-readable label for an Open-Meteo weather code."""
    lang = _lang(lang)
    return WEATHER_CODE_LABELS[lang].get(code, WEATHER_CODE_FALLBACK[lang])
