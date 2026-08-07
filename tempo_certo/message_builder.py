"""Notification message building."""

from datetime import datetime
from zoneinfo import ZoneInfo

from . import config, i18n
from .i18n import t


def build_message(windows, clothing):
    today_label = i18n.date_label(datetime.now(ZoneInfo(config.TIMEZONE)))
    lines = []
    if config.GREETING_ENABLED:
        lines.append(i18n.greeting())
        lines.append("")
    lines.append(t("header", date=today_label))
    lines.append("")

    # Windows section
    lines.append(t("windows_section_title"))
    any_window_advice = False

    if windows["is_hot"]:
        any_window_advice = True
        lines.append(
            t(
                "hot_close",
                close_hour=windows["hot_close_hour"],
                max_temp=round(windows["day_max_temp"]),
                max_temp_hour=windows["max_temp_hour"],
            )
        )
        if windows["hot_reopen_hour"]:
            lines.append(t("hot_reopen", reopen_hour=windows["hot_reopen_hour"]))
        else:
            lines.append(t("hot_no_reopen"))

    if windows["is_cold_windy"]:
        any_window_advice = True
        lines.append(
            t("cold_windy", start=windows["cold_windy_start"], end=windows["cold_windy_end"])
        )

    if not any_window_advice:
        lines.append(t("no_window_advice", max_temp=round(windows["day_max_temp"])))

    lines.append("")

    # Clothing section
    lines.append(t("clothing_section_title"))
    lines.append(
        t(
            "clothing_summary",
            sky=clothing["sky"].capitalize(),
            min_temp=round(clothing["day_min_temp"]),
            max_temp=round(clothing["day_max_temp"]),
            feels_max=round(clothing["feels_max"]),
        )
    )
    for a in clothing["advice"]:
        lines.append(f"• {a}")

    return "\n".join(lines)
