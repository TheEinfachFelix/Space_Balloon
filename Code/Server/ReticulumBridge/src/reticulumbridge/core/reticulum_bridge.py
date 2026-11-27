from __future__ import annotations

import RNS
from loguru import logger
from reticulumbridge.core.reticulum_router import reticulum_response_route
from reticulumbridge.models import CommandData


_RETICULUM_TO_LOGURU_LEVEL = {
    RNS.LOG_CRITICAL: 'CRITICAL',
    RNS.LOG_ERROR: 'ERROR',
    RNS.LOG_WARNING: 'WARNING',
    RNS.LOG_NOTICE: 'INFO',
    RNS.LOG_INFO: 'INFO',
    RNS.LOG_VERBOSE: 'DEBUG',
    RNS.LOG_DEBUG: 'DEBUG',
    RNS.LOG_PATHING: 'DEBUG',
    RNS.LOG_EXTREME: 'DEBUG',
}

_LOGURU_TO_RETICULUM_LEVEL = {
    'CRITICAL': RNS.LOG_CRITICAL,
    'ERROR': RNS.LOG_ERROR,
    'WARNING': RNS.LOG_WARNING,
    'INFO': RNS.LOG_INFO,
    'DEBUG': RNS.LOG_DEBUG,
}


def _reticulum_log(message: str) -> None:
    for reticulum_level, loguru_level in _RETICULUM_TO_LOGURU_LEVEL.items():
        label = RNS.loglevelname(reticulum_level)
        if label in message:
            log_message = message.split(label, 1)[1].strip()
            logger.log(loguru_level, log_message)
            return

    logger.warning('Unrecognized Reticulum log message format: {}', message)


class ReticulumBridge:
    def __init__(self):
        logger.info('ReticulumBridge wird initialisiert...')
        from reticulumbridge.dependencies import get_settings
        settings = get_settings()

        self.reticulum = RNS.Reticulum(
            configdir=settings.reticulum_bridge.reticulum.config_path,
            logdest=_reticulum_log,
            loglevel=_LOGURU_TO_RETICULUM_LEVEL[
                settings.reticulum_bridge.logging_level
            ],
        )

        # Initialize ReticulumBridge components here
        logger.success('ReticulumBridge erfolgreich initialisiert.')

    def __del__(self):
        logger.info('ReticulumBridge wird beendet...')
        # Clean up resources
        logger.success('ReticulumBridge erfolgreich beendet.')

    @reticulum_response_route('send')
    def sendMsg(self, data: CommandData) -> None:
        # Daten Komprimieren und senden
        pass

    # Empfangene Daten werden dekomprimiert und an den Router geleitet
