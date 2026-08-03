#!/usr/bin/env python3
"""
Tempo Certo
===========
Sends a daily Telegram notification with:
  1. Whether to close/reopen the shutters and windows, and when:
     - hot weather -> when to close (before peak heat) and reopen in the evening
     - cold + windy weather -> when to keep windows closed to avoid drafts/heat loss
  2. What to wear given the day's weather

Uses the free Open-Meteo API (no API key required).
Notification sent via Telegram by default. ntfy.sh and email (SMTP) are
available as alternatives — see config.py.

Meant to run via cron:
  0 6 * * 1-5    -> 6:00 AM on weekdays
  30 7 * * 6,0   -> 7:30 AM on weekends
"""

import sys
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
from zoneinfo import ZoneInfo

import requests

import config


# ---------------------------------------------------------------------------
# 1. Weather fetching (Open-Meteo, free, no API key)
# ---------------------------------------------------------------------------

def fetch_forecast():
    """Fetch today's hourly forecast for the configured location."""
    params = {
        "latitude": config.LATITUDE,
        "longitude": config.LONGITUDE,
        "hourly": "temperature_2m,apparent_temperature,precipitation_probability,"
                  "weathercode,wind_speed_10m,uv_index",
        "timezone": config.TIMEZONE,
        "forecast_days": 1,
    }
    resp = requests.get("https://api.open-meteo.com/v1/forecast", params=params, timeout=15)
    resp.raise_for_status()
    return resp.json()


def hours_today(data):
    """Return a list of dicts {hour, temp, feels_like, rain_prob, wind, uv, code} for today."""
    hourly = data["hourly"]
    today_str = datetime.now(ZoneInfo(config.TIMEZONE)).date().isoformat()
    result = []
    for i, ts in enumerate(hourly["time"]):
        if ts.startswith(today_str):
            result.append({
                "hour": int(ts[11:13]),
                "temp": hourly["temperature_2m"][i],
                "feels_like": hourly["apparent_temperature"][i],
                "rain_prob": hourly["precipitation_probability"][i],
                "wind": hourly["wind_speed_10m"][i],
                "uv": hourly["uv_index"][i],
                "code": hourly["weathercode"][i],
            })
    return result


# ---------------------------------------------------------------------------
# 2. Shutters / windows logic
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# 3. Clothing advice logic
# ---------------------------------------------------------------------------

FRENCH_WEEKDAYS = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
FRENCH_MONTHS = [
    "janvier", "février", "mars", "avril", "mai", "juin",
    "juillet", "août", "septembre", "octobre", "novembre", "décembre",
]


def french_date_label(dt):
    """Format a date in French without depending on the system locale."""
    return f"{FRENCH_WEEKDAYS[dt.weekday()]} {dt.day:02d} {FRENCH_MONTHS[dt.month - 1]} {dt.year}"


WEATHER_CODE_LABELS = {
    0: "ciel dégagé", 1: "plutôt dégagé", 2: "partiellement nuageux", 3: "couvert",
    45: "brouillard", 48: "brouillard givrant",
    51: "bruine légère", 53: "bruine", 55: "bruine forte",
    61: "pluie légère", 63: "pluie", 65: "pluie forte",
    71: "neige légère", 73: "neige", 75: "neige forte",
    80: "averses légères", 81: "averses", 82: "averses fortes",
    95: "orages", 96: "orages avec grêle", 99: "orages violents",
}


def analyze_clothing(hours):
    """Build clothing advice from the day's weather."""
    if not hours:
        return None

    temps = [h["temp"] for h in hours]
    feels = [h["feels_like"] for h in hours]
    rain_probs = [h["rain_prob"] for h in hours]
    winds = [h["wind"] for h in hours]
    uvs = [h["uv"] for h in hours]
    codes = [h["code"] for h in hours]

    day_min, day_max = min(temps), max(temps)
    feels_max = max(feels)
    max_rain_prob = max(rain_probs)
    max_wind = max(winds)
    max_uv = max(uvs)
    dominant_code = max(set(codes), key=codes.count)

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


# ---------------------------------------------------------------------------
# 4. Message building
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# 5. Sending the notification
# ---------------------------------------------------------------------------

def strip_markdown(text):
    """Drop the *bold* markers used for Telegram; plain-text channels don't render them."""
    return text.replace("*", "")


def send_telegram(message):
    url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendMessage"
    resp = requests.post(
        url,
        data={"chat_id": config.TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"},
        timeout=10,
    )
    resp.raise_for_status()


def send_ntfy(message):
    url = f"https://ntfy.sh/{config.NTFY_TOPIC}"
    requests.post(
        url,
        data=strip_markdown(message).encode("utf-8"),
        headers={"Title": "Tempo Certo", "Tags": "sunny,shirt"},
        timeout=10,
    )


def send_email(message):
    msg = MIMEText(strip_markdown(message))
    msg["Subject"] = "Tempo Certo — conseils du jour"
    msg["From"] = config.SMTP_FROM
    msg["To"] = config.SMTP_TO

    with smtplib.SMTP(config.SMTP_HOST, config.SMTP_PORT) as server:
        server.starttls()
        server.login(config.SMTP_USER, config.SMTP_PASSWORD)
        server.sendmail(config.SMTP_FROM, [config.SMTP_TO], msg.as_string())


def notify(message):
    if config.NOTIFY_METHOD == "telegram":
        send_telegram(message)
    elif config.NOTIFY_METHOD == "ntfy":
        send_ntfy(message)
    elif config.NOTIFY_METHOD == "email":
        send_email(message)
    else:
        raise ValueError(f"Unknown notification method: {config.NOTIFY_METHOD}")


# ---------------------------------------------------------------------------
# 6. Main
# ---------------------------------------------------------------------------

def main():
    try:
        data = fetch_forecast()
        hours = hours_today(data)
        if not hours:
            print("No hourly data available for today.", file=sys.stderr)
            sys.exit(1)

        windows = analyze_windows(hours)
        clothing = analyze_clothing(hours)
        message = build_message(windows, clothing)

        print(message)  # useful for cron logs
        notify(message)

    except requests.RequestException as e:
        print(f"Network error while calling the weather API or notification service: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
