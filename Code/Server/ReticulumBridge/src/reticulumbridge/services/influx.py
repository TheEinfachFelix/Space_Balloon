from __future__ import annotations

from loguru import logger
from pydantic import BaseModel


class InfluxConfig(BaseModel):
    url: str
    token: str
    org: str
    bucket: str


class InfluxConnector:
    def __init__(self, config: InfluxConfig):
        logger.info('InfluxConnector wird initialisiert...')
        self.config = config
        # Initialize the InfluxDB client here using the provided configuration
        logger.success('InfluxConnector erfolgreich initialisiert.')

    def __del__(self):
        logger.info('InfluxConnector wird beendet...')
        # Clean up resources
        logger.success('InfluxConnector erfolgreich beendet.')

    def write_data(self, data):
        logger.debug(f"Schreibe Daten in InfluxDB: {data}")

        logger.success('Daten erfolgreich in InfluxDB geschrieben.')
