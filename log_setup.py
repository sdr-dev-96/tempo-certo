"""Logging configuration for Tempo Certo."""

import logging


def setup_logging():
    """Configure the root logger for CLI/cron usage and return the app logger."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    return logging.getLogger("tempo_certo")
