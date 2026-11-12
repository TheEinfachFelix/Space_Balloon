from __future__ import annotations

from influxdb_client.client.influxdb_client import InfluxDBClient
from loguru import logger
from reticulumbridge.models import TelemetryData


class InfluxConnector:
    def __init__(self) -> None:
        logger.info('InfluxConnector wird initialisiert...')
        from reticulumbridge.dependencies import get_settings
        settings = get_settings()

        self.url = settings.influxdb_shared_config.url
        self.token = settings.reticulum_bridge.influxdb.token
        self.org = settings.influxdb_shared_config.org
        self.bucket = settings.influxdb_shared_config.bucket
        self.measurement = (
            settings.reticulum_bridge.
            influxdb.telemetry_measurement
        )

        self.client = InfluxDBClient(
            url=self.url,
            token=self.token,
            org=self.org,
        )
        logger.success('InfluxConnector erfolgreich initialisiert.')

    def __del__(self) -> None:
        logger.info('InfluxConnector wird beendet...')
        try:
            if hasattr(self, 'client') and self.client:
                self.client.close()
            logger.success('InfluxConnector erfolgreich beendet.')
        except Exception as e:
            logger.error(f"Fehler beim Schließen des InfluxDB-Clients: {e}")

    def write_data(self, telemetry_data: TelemetryData) -> None:
        logger.debug(f"Schreibe Daten in InfluxDB: {telemetry_data}")
        try:
            node_name = str(telemetry_data.node_name)
            timestamp = telemetry_data.timestamp

            fields = telemetry_data.model_dump(
                exclude={'node_name', 'timestamp'},
            )

            record = {
                'measurement': self.measurement,
                'tags': {'node_name': node_name},
                'fields': fields,
                'time': timestamp,
            }

            write_api = self.client.write_api()
            write_api.write(
                bucket=self.bucket,
                org=self.org,
                record=record,
            )
            logger.debug('Daten erfolgreich in InfluxDB geschrieben')

        except Exception as e:
            logger.error(f"Fehler beim Schreiben in InfluxDB: {e}")
            raise
