"""Logging configuration for Tempo Certo."""

import logging
import sys
from datetime import date
from pathlib import Path

import config


def setup_logging():
    """Configure logging: one file per day in LOG_DIR, plus stdout (for cron)."""
    log_dir = Path(config.LOG_DIR)
    log_dir.mkdir(parents=True, exist_ok=True)

    log_file = log_dir / f"{date.today().isoformat()}.log"

    logger = logging.getLogger("tempo_certo")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()  # avoid duplicate handlers if setup_logging is called twice in a process

    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", datefmt="%H:%M:%S")

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    cleanup_old_logs(log_dir)
    return logger


def cleanup_old_logs(log_dir):
    """Delete daily log files older than config.LOG_RETENTION_DAYS."""
    cutoff = date.today().toordinal() - config.LOG_RETENTION_DAYS
    for log_file in log_dir.glob("*.log"):
        try:
            file_date = date.fromisoformat(log_file.stem)
            if file_date.toordinal() < cutoff:
                log_file.unlink()
        except ValueError:
            continue  # not a YYYY-MM-DD.log file, leave it alone
