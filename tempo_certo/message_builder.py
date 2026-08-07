"""Notification message building."""

from datetime import datetime
from zoneinfo import ZoneInfo

from . import config, i18n
from .i18n import t


def _accroche(today_label):
    parts = []
    if config.GREETING_ENABLED:
        parts.append(i18n.greeting_word())
    if config.USER_FIRST_NAME:
        parts.append(config.USER_FIRST_NAME)
    prefix = ", ".join(parts)
    if prefix:
        return t("accroche_prefixed", prefix=prefix, date=today_label)
    return t("accroche_plain", date=today_label)


def _today_section(clothing):
    sentence = t(
        "today_summary",
        sky=clothing["sky"].capitalize(),
        min_temp=round(clothing["day_min_temp"]),
        max_temp=round(clothing["day_max_temp"]),
        feels_max=round(clothing["feels_max"]),
    )
    if clothing["temp_swing"]:
        sentence += " " + t("temp_swing")
    return sentence


def _clothing_section(clothing):
    return " ".join(clothing["advice"])


def _windows_section(windows):
    sentences = []

    if windows["is_hot"]:
        sentence = t(
            "hot_close",
            close_hour=windows["hot_close_hour"],
            max_temp=round(windows["day_max_temp"]),
            max_temp_hour=windows["max_temp_hour"],
        )
        if windows["hot_reopen_hour"]:
            sentence += t("hot_reopen", reopen_hour=windows["hot_reopen_hour"])
        else:
            sentence += t("hot_no_reopen")
        sentences.append(sentence)

    if windows["is_cold_windy"]:
        sentences.append(
            t("cold_windy", start=windows["cold_windy_start"], end=windows["cold_windy_end"])
        )

    if not sentences:
        sentences.append(t("no_window_advice", max_temp=round(windows["day_max_temp"])))

    return " ".join(sentences)


def build_message(windows, clothing):
    today_label = datetime.now(ZoneInfo(config.TIMEZONE)).strftime(config.DATE_FORMAT)

    lines = [
        _accroche(today_label),
        "",
        t("today_title"),
        _today_section(clothing),
        "",
        t("clothing_title"),
        _clothing_section(clothing),
        "",
        t("windows_title"),
        _windows_section(windows),
    ]

    return "\n".join(lines)
