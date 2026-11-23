from __future__ import annotations

from influxdb_client.client.influxdb_client import InfluxDBClient
from loguru import logger
from reticulumbridge.core.reticulum_router import reticulum_response_route
from reticulumbridge.models import TelemetryData, ResponseData, CommandData


class InfluxConnector:
    def __init__(self) -> None:
        logger.info('InfluxConnector wird initialisiert...')
        from reticulumbridge.dependencies import get_settings
        settings = get_settings()

        self.url = settings.influxdb_shared_config.url
        self.token = settings.reticulum_bridge.influxdb.token

        self.org = settings.influxdb_shared_config.org
        self.bucket = settings.influxdb_shared_config.bucket
        self.telemetry_measurement = (
            settings.reticulum_bridge.
            influxdb.telemetry_measurement
        )
        self.command_measurement = (
            settings.reticulum_bridge.
            influxdb.command_measurement
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

    def _write_to_db(self, node_name: str, timestamp: str, fields: dict, measurement: str) -> None:
        logger.debug(f"Schreibe Daten in InfluxDB: {node_name}, {timestamp}, {fields}")
        try:
            record = {
                'measurement': measurement,
                'tags': {'node_name': node_name},
                'fields': fields,
                'time': timestamp,
            }

            write_api = self.client.write_api(
                error_callback=self._log_async_write_error,
            )
            write_api.write(
                bucket=self.bucket,
                org=self.org,
                record=record,
            )
            logger.debug('Daten erfolgreich in InfluxDB geschrieben')

        except Exception as e:
            logger.error(f"Fehler beim Schreiben in InfluxDB: {e}")
            raise

    @reticulum_response_route('telemetry')
    def write_telemetry(self, telemetry_data: TelemetryData) -> None:
        node_name = str(telemetry_data.node_name)
        timestamp = telemetry_data.timestamp

        fields = telemetry_data.model_dump(
            exclude={'node_name', 'timestamp'},
        )

        self._write_to_db(node_name, timestamp, fields, self.telemetry_measurement)

    @reticulum_response_route('response')
    def write_response(self, response_data: ResponseData) -> None:
            
        node_name = str(response_data.node_name)
        timestamp = response_data.timestamp

        fields = response_data.model_dump(
            exclude={'node_name', 'timestamp','result'},
        )
        fields['result'] = str(response_data.result)

        self._write_to_db(node_name, timestamp, fields, self.command_measurement)

    @reticulum_response_route('send')
    def write_send(self, send_data: CommandData) -> None:
            
        node_name = str(send_data.node_name)
        timestamp = send_data.timestamp

        fields = send_data.model_dump(
            exclude={'node_name', 'timestamp','parameters'},
        )
        fields['parameters'] = str(send_data.parameters)

        self._write_to_db(node_name, timestamp, fields, self.command_measurement)

    @staticmethod
    def _log_async_write_error(
        _conf: str,
        _data: str,
        exception: Exception,
    ) -> None:
        logger.opt(exception=exception).error(
            'Fehler beim asynchronen Schreiben in InfluxDB',
        )
