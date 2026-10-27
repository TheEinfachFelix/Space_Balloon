from __future__ import annotations

import logging
import sys

from controllcenter.config import Settings
from loguru import logger


class StreamToLogger:
    """Leitet Ausgaben von stdout/stderr
    (z.B. print oder Streamlit-Banner) an Loguru weiter."""

    def __init__(self, original_stream, level: str = 'INFO'):
        self.original_stream = original_stream
        self.level = level

    def write(self, buffer: str) -> None:
        for line in buffer.rstrip().splitlines():
            if line.strip():
                # depth=2 sorgt dafür, dass der Aufrufer korrekt erkannt wird
                logger.opt(depth=2).log(self.level, line.strip())

    def flush(self) -> None:
        self.original_stream.flush()


def _set_loguru_as_default_logger(log_level: str) -> None:
    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.setLevel(log_level)

    class InterceptHandler(logging.Handler):
        def emit(self, record: logging.LogRecord) -> None:
            try:
                level = logger.level(record.levelname).name
            except ValueError:
                level = record.levelno

            frame, depth = logging.currentframe(), 2
            while (
                frame.f_back and
                frame.f_code.co_filename == logging.__file__
            ):
                frame = frame.f_back
                depth += 1

            logger.opt(depth=depth, exception=record.exc_info).log(
                level, record.getMessage(),
            )

    root_logger.addHandler(InterceptHandler())


def setup_logging(settings: Settings) -> None:
    """Konfiguriert Loguru und fängt Standard-Logs sowie stdout/stderr ab."""
    log_level = settings.controllcenter_config.logging_level

    # Original-Streams sichern, um Endlosschleifen zu verhindern
    original_stderr = sys.stderr
    original_stdout = sys.stdout

    # Loguru zurücksetzen und Handler auf den *originalen* stderr legen
    logger.remove()
    logger.add(original_stderr, level=log_level)

    # Standard-Logging abfangen
    _set_loguru_as_default_logger(log_level)

    # sys.stdout und sys.stderr umleiten,
    # damit Streamlit/Uvicorn-Meldungen im Loguru-Format erscheinen
    sys.stdout = StreamToLogger(original_stdout, level='INFO')
    sys.stderr = StreamToLogger(original_stderr, level='INFO')
