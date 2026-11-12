from __future__ import annotations

from datetime import datetime
from datetime import timezone
from unittest.mock import MagicMock

import pytest
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


def test_influx_connector_write_data_uses_correct_parameters(
        mock_settings,
        mock_influx_client,
):
    """Testet, ob write_data das TelemetryData-Model korrekt verarbeitet"""
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
    connector.write_data(telemetry_data)

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


def test_influx_connector_write_data_handles_error(
        influx_connector,
        mock_influx_client,
):
    """Testet das Verhalten, wenn beim Schreiben ein Fehler auftritt."""
    _, mock_write_api, _ = mock_influx_client
    mock_write_api.write.side_effect = Exception('Connection lost')

    telemetry_data = MagicMock()

    with pytest.raises(Exception, match='Connection lost'):
        influx_connector.write_data(telemetry_data)
