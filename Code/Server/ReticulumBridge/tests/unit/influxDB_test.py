from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from datetime import timezone
from types import SimpleNamespace
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest
from influxdb_client.client.write_api import SYNCHRONOUS
from reticulumbridge.services.influx import InfluxConnector


def test_influx_connector_init_uses_config(
        influx_connector,
        mock_settings,
        mock_influx_client,
):
    """Testet, ob der Constructor den InfluxDB-Client
    korrekt aus den Settings initialisiert hat."""
    _, _, mock_cls = mock_influx_client
    mock_cls.assert_called_once_with(
        url=mock_settings.influxdb_shared_config.url,
        token=mock_settings.reticulum_bridge.influxdb.token,
        org=mock_settings.influxdb_shared_config.org,
    )


def test_influx_connector_write_telemetry_uses_correct_parameters(
        mock_settings,
        mock_influx_client,
):
    """Testet, ob write_telemetry das
    TelemetryData-Model korrekt verarbeitet"""
    mock_client, mock_write_api, _ = mock_influx_client

    expected_measurement = 'space_balloon_telemetry'
    mock_settings.reticulum_bridge.influxdb.telemetry_measurement = (
        expected_measurement
    )

    connector = InfluxConnector()

    # TelemetryData-Modell simulieren
    test_timestamp = datetime(2026, 11, 12, 18, 0, 0, tzinfo=timezone.utc)
    test_node_name = 'node-alpha-01'

    telemetry_data = MagicMock()
    telemetry_data.timestamp = test_timestamp
    telemetry_data.node_name = test_node_name
    telemetry_data.temperature = 21.5
    telemetry_data.pressure = 1013.25

    # Methode aufrufen
    connector.write_telemetry(telemetry_data)

    # Prüfen, ob die Write-API aufgerufen wurde
    mock_client.write_api.assert_called_once()
    mock_write_api.write.assert_called_once()

    # Überprüfen der übergebenen Argumente
    call_kwargs = mock_write_api.write.call_args.kwargs

    assert call_kwargs['bucket'] == mock_settings.influxdb_shared_config.bucket
    assert call_kwargs['org'] == mock_settings.influxdb_shared_config.org

    record = call_kwargs['record']
    if isinstance(record, dict):
        assert record.get('measurement') == expected_measurement
        assert record.get('tags', {}).get('node_name') == test_node_name
        assert record.get('time') == test_timestamp


def test_influx_connector_destructor_closes_connection(
        influx_connector,
        mock_influx_client,
):
    """Testet, ob der Destruktor (__del__) die Verbindung sauber schließt."""
    mock_client, _, _ = mock_influx_client
    influx_connector.__del__()
    mock_client.close.assert_called_once()


def test_influx_connector_write_telemetry_handles_error(
        influx_connector,
        mock_influx_client,
):
    """Testet das Verhalten, wenn beim Schreiben ein Fehler auftritt."""
    _, mock_write_api, _ = mock_influx_client
    mock_write_api.write.side_effect = Exception('Connection lost')

    telemetry_data = MagicMock()

    with pytest.raises(Exception, match='Connection lost'):
        influx_connector.write_telemetry(telemetry_data)


def test_influx_connector_logs_async_write_error(
        influx_connector,
        mock_influx_client,
):
    mock_client, _, _ = mock_influx_client
    influx_connector.write_telemetry(MagicMock())
    error_callback = mock_client.write_api.call_args.kwargs['error_callback']
    error = Exception('Unauthorized')

    with patch('reticulumbridge.services.influx.logger') as mock_logger:
        error_callback('config', 'data', error)

    mock_logger.opt.assert_called_once_with(exception=error)
    mock_logger.opt.return_value.error.assert_called_once_with(
        'Fehler beim asynchronen Schreiben in InfluxDB',
    )


def test_generate_id_is_sequential_persistent_and_locked(
        mock_settings,
        mock_influx_client,
):
    mock_client, _, _ = mock_influx_client
    persisted_ids = []

    class FakeQueryApi:
        def query(self, query, org):
            assert org == mock_settings.influxdb_shared_config.org
            assert (
                mock_settings.reticulum_bridge.influxdb.command_id_measurement
                in query
            )
            assert 'max(column: "_value")' in query
            assert 'group(columns: [])' in query
            current_id = persisted_ids[-1] if persisted_ids else None
            if current_id is None:
                return []
            return [
                SimpleNamespace(
                    records=[
                        SimpleNamespace(
                            values={'_value': current_id},
                            get_value=lambda: current_id,
                        ),
                    ],
                ),
            ]

    class FakeWriteApi:
        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return None

        def write(self, bucket, org, record):
            assert bucket == mock_settings.influxdb_shared_config.bucket
            assert org == mock_settings.influxdb_shared_config.org
            influx_settings = mock_settings.reticulum_bridge.influxdb
            assert (
                record['measurement']
                == influx_settings.command_id_measurement
            )
            persisted_ids.append(record['fields']['id'])

    mock_client.query_api.return_value = FakeQueryApi()
    mock_client.write_api.return_value = FakeWriteApi()

    connector = InfluxConnector()
    with ThreadPoolExecutor(max_workers=8) as executor:
        generated_ids = list(
            executor.map(
                lambda _: connector.generate_id(),
                range(20),
            ),
        )

    assert sorted(generated_ids) == list(range(1, 21))
    mock_client.write_api.assert_called()
    assert all(
        call.kwargs['write_options'] is SYNCHRONOUS
        for call in mock_client.write_api.call_args_list
    )
