from __future__ import annotations

import pytest


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
        token=mock_settings.reticulum_bridge.influxdb_token,
        org=mock_settings.influxdb_shared_config.org,
    )


def test_influx_connector_write_data(
        influx_connector,
        mock_settings,
        mock_influx_client,
):
    """Testet das erfolgreiche Schreiben von Daten über die Write-API."""
    mock_client, mock_write_api, _ = mock_influx_client
    test_data = {'measurement': 'sensor_data', 'fields': {'value': 42.0}}

    influx_connector.write_data(test_data)

    mock_client.write_api.assert_called_once()
    mock_write_api.write.assert_called_once_with(
        bucket=mock_settings.influxdb_shared_config.bucket,
        org=mock_settings.influxdb_shared_config.org,
        record=test_data,
    )


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

    with pytest.raises(Exception, match='Connection lost'):
        influx_connector.write_data({'measurement': 'test'})
