from __future__ import annotations

from loguru import logger
from pydantic import BaseModel
from influxdb_client.client.influxdb_client import InfluxDBClient 

class InfluxConfig(BaseModel):
    url: str
    token: str
    org: str
    bucket: str


class InfluxConnector:
    def __init__(self, config: InfluxConfig):
        logger.info('InfluxConnector wird initialisiert...')
        self.config = config
        self.client = InfluxDBClient(
            url=self.config.url,
            token=self.config.token,
            org=self.config.org
        )
        self.write_api = self.client.write_api()
        logger.success('InfluxConnector erfolgreich initialisiert.')

    def __del__(self):
        logger.info('InfluxConnector wird beendet...')
        self.client.close()
        logger.success('InfluxConnector erfolgreich beendet.')

    def write_data(self, data):
        logger.debug(f"Schreibe Daten in InfluxDB: {data}")

        self.write_api.write(
            bucket=self.config.bucket,
            org=self.config.org,
            record=data
        )
        logger.success('Daten erfolgreich in InfluxDB geschrieben.')
