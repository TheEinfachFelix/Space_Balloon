from __future__ import annotations

from influxdb_client.client.influxdb_client import InfluxDBClient
from loguru import logger


class InfluxConnector:
    def __init__(self):
        logger.info('InfluxConnector wird initialisiert...')
        from reticulumbridge.dependencies import get_settings
        settings = get_settings()

        self.client = InfluxDBClient(
            url=settings.influxdb_shared_config.url,
            token=settings.reticulum_bridge.influxdb_token,
            org=settings.influxdb_shared_config.org,
        )
        self.write_api = self.client.write_api()
        logger.success('InfluxConnector erfolgreich initialisiert.')

    def __del__(self):
        logger.info('InfluxConnector wird beendet...')
        self.client.close()
        logger.success('InfluxConnector erfolgreich beendet.')

    def write_data(self, data):
        logger.debug(f"Schreibe Daten in InfluxDB: {data}")
        from reticulumbridge.dependencies import get_settings
        settings = get_settings()

        self.write_api.write(
            bucket=settings.influxdb_shared_config.bucket,
            org=settings.influxdb_shared_config.org,
            record=data,
        )
        logger.debug('Daten erfolgreich in InfluxDB geschrieben')
