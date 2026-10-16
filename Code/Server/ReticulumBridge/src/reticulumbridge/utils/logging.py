from __future__ import annotations

import logging
import sys

from loguru import logger
from reticulumbridge.config import Settings


def _set_loguru_as_default_logger(log_level: str) -> None:
    # Remove existing handlers
    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.setLevel(log_level)

    class InterceptHandler(logging.Handler):
        def emit(self, record: logging.LogRecord) -> None:
            # Get corresponding Loguru level
            try:
                level = logger.level(record.levelname).name
            except ValueError:
                level = record.levelno

            # Find caller to get correct stack depth
            frame, depth = logging.currentframe(), 2
            while (
                frame.f_back
                and frame.f_code.co_filename == logging.__file__
            ):
                frame = frame.f_back
                depth += 1

            logger.opt(depth=depth, exception=record.exc_info).log(
                level, record.getMessage(),
            )

    # Intercept standard logging
    root_logger.addHandler(InterceptHandler())


def setup_logging(settings: Settings) -> None:
    """Konfiguriert Loguru basierend auf dem Log-Level aus der config.yml."""
    log_level = settings.reticulum_bridge.logging_level
    _set_loguru_as_default_logger(log_level)
    logger.remove()  # Standard-Handler entfernen

    logger.add(
        sys.stdout,
        level=log_level,
        format='<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | '
        '<level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}'
        '</cyan>:<cyan>{line}</cyan> - <level>{message}</level>',
    )
    logger.info(f"Logging initialisiert. Aktuelles Level: {log_level}")

    loggers = (
        'uvicorn',
        'uvicorn.access',
        'uvicorn.error',
        'fastapi',
        'asyncio',
        'starlette',
    )

    for logger_name in loggers:
        logging_logger = logging.getLogger(logger_name)
        logging_logger.handlers = []
        logging_logger.propagate = True
