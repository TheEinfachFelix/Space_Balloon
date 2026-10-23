from __future__ import annotations

from unittest.mock import patch

from controllcenter.models import TelemetryData
from controllcenter.repository import ReticulumBridgeEndpoints


def test_get_telemetry_calls_correct_endpoint(bridge):
    expected_result = object()

    with patch.object(
        bridge,
        '_http_get',
        return_value=expected_result,
    ) as mock_http_get:
        result = bridge.get_telemetry()

    mock_http_get.assert_called_once_with(
        ReticulumBridgeEndpoints.telemetry,
        [],
        TelemetryData,
    )
    assert result is expected_result
