"""Notification message building."""

from datetime import datetime
from zoneinfo import ZoneInfo

import config

FRENCH_WEEKDAYS = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
FRENCH_MONTHS = [
    "janvier", "février", "mars", "avril", "mai", "juin",
    "juillet", "août", "septembre", "octobre", "novembre", "décembre",
]

WEATHER_CODE_LABELS = {
    0: "ciel dégagé", 1: "plutôt dégagé", 2: "partiellement nuageux", 3: "couvert",
    45: "brouillard", 48: "brouillard givrant",
    51: "bruine légère", 53: "bruine", 55: "bruine forte",
    61: "pluie légère", 63: "pluie", 65: "pluie forte",
    71: "neige légère", 73: "neige", 75: "neige forte",
    80: "averses légères", 81: "averses", 82: "averses fortes",
    95: "orages", 96: "orages avec grêle", 99: "orages violents",
}


def french_date_label(dt):
    """Format a date in French without depending on the system locale."""
    return f"{FRENCH_WEEKDAYS[dt.weekday()]} {dt.day:02d} {FRENCH_MONTHS[dt.month - 1]} {dt.year}"


def build_message(windows, clothing):
    today_label = french_date_label(datetime.now(ZoneInfo(config.TIMEZONE)))
    lines = [f"☀️ *Tempo Certo* — {today_label}", ""]

    # Windows section
    lines.append("*🪟 Volets / fenêtres*")
    any_window_advice = False

    if windows["is_hot"]:
        any_window_advice = True
        lines.append(
            f"• Chaleur : fermer vers *{windows['hot_close_hour']}h* "
            f"(pic à *{round(windows['day_max_temp'])}°C* vers {windows['max_temp_hour']}h)"
        )
        if windows["hot_reopen_hour"]:
            lines.append(f"• Réouverture possible vers *{windows['hot_reopen_hour']}h* en soirée")
        else:
            lines.append("• Garder fermé toute la soirée, la fraîcheur ne revient pas vite")

    if windows["is_cold_windy"]:
        any_window_advice = True
        lines.append(
            f"• Froid + vent : garder les fenêtres fermées entre *{windows['cold_windy_start']}h* "
            f"et *{windows['cold_windy_end']}h* pour éviter les déperditions de chaleur"
        )

    if not any_window_advice:
        lines.append(f"• Rien de particulier aujourd'hui (max {round(windows['day_max_temp'])}°C, peu de vent)")

    lines.append("")

    # Clothing section
    lines.append("*👕 Tenue du jour*")
    lines.append(
        f"{clothing['sky'].capitalize()}, {round(clothing['day_min_temp'])}°C → "
        f"{round(clothing['day_max_temp'])}°C (ressenti max {round(clothing['feels_max'])}°C)"
    )
    for a in clothing["advice"]:
        lines.append(f"• {a}")

    return "\n".join(lines)
