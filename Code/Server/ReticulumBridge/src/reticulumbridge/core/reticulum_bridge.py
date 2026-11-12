from __future__ import annotations

import RNS
from loguru import logger
from pydantic import BaseModel


class ReticulumBridge:
    def __init__(self):
        logger.info('ReticulumBridge wird initialisiert...')
        from reticulumbridge.dependencies import get_settings
        settings = get_settings()

        self.reticulum = RNS.Reticulum(
            # TODO Logging konfigurieren und path checken
            configdir=settings.reticulum_bridge.reticulum.config_path,
        )

        # Initialize ReticulumBridge components here
        logger.success('ReticulumBridge erfolgreich initialisiert.')

    def __del__(self):
        logger.info('ReticulumBridge wird beendet...')
        # Clean up resources
        logger.success('ReticulumBridge erfolgreich beendet.')

    async def sendMsg(self, data: BaseModel) -> None:
        # Daten Komprimieren und senden
        pass

    # Empfangene Daten werden dekomprimiert und an den Router geleitet
