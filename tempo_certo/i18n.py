"""Translations for the daily notification message."""

import random

from . import config

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

GREETINGS = {
    "fr": ["Bonjour", "Salut", "Coucou"],
    "en": ["Hello", "Hi", "Hey"],
}

STRINGS = {
    "fr": {
        "accroche_prefixed": "{prefix}, voici le récap météo d'aujourd'hui ({date}) :",
        "accroche_plain": "Voici le récap météo d'aujourd'hui ({date}) :",
        "today_title": "🌡️ Aujourd'hui",
        "today_summary": (
            "{sky}, avec des températures entre {min_temp}°C et {max_temp}°C "
            "(ressenti jusqu'à {feels_max}°C)."
        ),
        "temp_swing": (
            "L'écart de température est marqué : prévoyez une couche à "
            "enlever ou ajouter dans la journée."
        ),
        "clothing_title": "👕 Tenue",
        "outfit_very_light": "Tenue très légère (coton/lin), vêtements amples et clairs.",
        "outfit_light_summer": "Tenue légère d'été, manches courtes.",
        "outfit_light_evening_jacket": "Tenue légère, une petite veste peut suffire le soir.",
        "outfit_jacket_layers": "Prévoir une veste ou un pull, quelques couches.",
        "outfit_warm": "Habillage chaud : manteau, couches superposées.",
        "rain_high": "Le risque de pluie est élevé, mieux vaut prendre un parapluie ou un imperméable.",
        "rain_moderate": "Le risque de pluie est modéré, un parapluie de sécurité peut être utile.",
        "wind_strong": "Du vent fort est prévu, évitez les vêtements amples et les parapluies fragiles.",
        "wind_light": "Un peu de vent est prévu, une couche coupe-vent peut aider.",
        "uv_very_high": "L'indice UV est très élevé, crème solaire, chapeau et lunettes de soleil sont indispensables.",
        "uv_high": "L'indice UV est élevé, pensez à la protection solaire.",
        "windows_title": "🪟 Fenêtres",
        "hot_close": (
            "Il va faire chaud aujourd'hui, avec un pic à {max_temp}°C vers {max_temp_hour}h : "
            "pensez à fermer les fenêtres vers {close_hour}h."
        ),
        "hot_reopen": " Vous pourrez rouvrir en soirée, vers {reopen_hour}h.",
        "hot_no_reopen": " Mieux vaut tout garder fermé pour la soirée, la fraîcheur ne reviendra pas vite.",
        "cold_windy": (
            "Avec le froid et le vent annoncés, gardez les fenêtres fermées entre "
            "{start}h et {end}h pour limiter les déperditions de chaleur."
        ),
        "no_window_advice": "Rien de particulier à signaler côté fenêtres aujourd'hui (max {max_temp}°C, peu de vent).",
    },
    "en": {
        "accroche_prefixed": "{prefix}, here's today's weather recap ({date}):",
        "accroche_plain": "Here's today's weather recap ({date}):",
        "today_title": "🌡️ Today",
        "today_summary": (
            "{sky}, with temperatures between {min_temp}°C and {max_temp}°C "
            "(feels like up to {feels_max}°C)."
        ),
        "temp_swing": (
            "The temperature swing is significant, so plan a layer you can "
            "add or remove during the day."
        ),
        "clothing_title": "👕 Outfit",
        "outfit_very_light": "Very light outfit (cotton/linen), loose and light-colored clothes.",
        "outfit_light_summer": "Light summer outfit, short sleeves.",
        "outfit_light_evening_jacket": "Light outfit, a light jacket may help in the evening.",
        "outfit_jacket_layers": "Bring a jacket or sweater, a few layers.",
        "outfit_warm": "Dress warmly: coat, layered clothing.",
        "rain_high": "The chance of rain is high, so an umbrella or raincoat is recommended.",
        "rain_moderate": "There's a moderate chance of rain, so a backup umbrella could help.",
        "wind_strong": "Strong wind is expected, so avoid loose clothing and flimsy umbrellas.",
        "wind_light": "A bit of wind is expected, so a windbreaker layer can help.",
        "uv_very_high": "The UV index is very high, so sunscreen, a hat and sunglasses are essential.",
        "uv_high": "The UV index is high, so consider sun protection.",
        "windows_title": "🪟 Windows",
        "hot_close": (
            "It's going to be hot today, peaking at {max_temp}°C around {max_temp_hour}h: "
            "consider closing the windows around {close_hour}h."
        ),
        "hot_reopen": " You'll be able to reopen in the evening, around {reopen_hour}h.",
        "hot_no_reopen": " Better keep everything closed for the evening, it won't cool down quickly.",
        "cold_windy": (
            "With cold and wind expected, keep the windows closed between "
            "{start}h and {end}h to limit heat loss."
        ),
        "no_window_advice": "Nothing special to report for the windows today (max {max_temp}°C, little wind).",
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


def greeting_word(lang=None):
    """Return a random greeting word, without punctuation (e.g. "Bonjour")."""
    lang = _lang(lang)
    return random.choice(GREETINGS[lang])
