# tests/test_reticulum_bridge_utils.py
from __future__ import annotations

from unittest.mock import Mock
from unittest.mock import patch

import pytest
import requests
from conftest import ExampleResponse
from controllcenter.repository import (
    ReticulumBridgeEndpoints,
)
from pydantic import ValidationError


def test_build_url_without_params(bridge):
    endpoint = Mock(spec=ReticulumBridgeEndpoints.telemetry)
    endpoint.value = 'telemetry'

    result = bridge._build_url(endpoint, [])

    assert result == 'https://example.invalid/api/telemetry'


def test_build_url_replaces_params_in_order(bridge):
    endpoint = Mock(spec=ReticulumBridgeEndpoints.telemetry)
    endpoint.value = 'devices/{}/telemetry/{}'

    result = bridge._build_url(endpoint, ['device-42', 'temperature'])

    assert result == (
        'https://example.invalid/api/'
        'devices/device-42/telemetry/temperature'
    )


def test_cast_response_returns_pydantic_model(bridge, response):
    result = bridge._cast_response(response, ExampleResponse)

    assert result == ExampleResponse(status='ok')
    assert isinstance(result, ExampleResponse)


def test_cast_response_rejects_invalid_data(bridge, response):
    response.json.return_value = {'unexpected': 'value'}

    with pytest.raises(ValidationError):
        bridge._cast_response(response, ExampleResponse)


def test_http_get_calls_correct_url_and_casts_response(
    bridge,
    response,
):
    endpoint = Mock(spec=ReticulumBridgeEndpoints.telemetry)
    expected_model = ExampleResponse
    expected_result = ExampleResponse(status='ok')

    with (
        patch(
            'controllcenter.repository.reticulum_api.requests.get',
            return_value=response,
        ) as mock_get,
        patch.object(
            bridge,
            '_build_url',
            return_value='https://example.invalid/test',
        ) as mock_build_url,
        patch.object(
            bridge,
            '_cast_response',
            return_value=expected_result,
        ) as mock_cast,
    ):
        result = bridge._http_get(endpoint, [], expected_model)

    mock_build_url.assert_called_once_with(endpoint, [])
    mock_get.assert_called_once_with('https://example.invalid/test')
    mock_cast.assert_called_once_with(response, expected_model)
    assert result is expected_result


def test_http_get_propagates_http_error(bridge, response):
    endpoint = Mock(spec=ReticulumBridgeEndpoints.telemetry)
    response.raise_for_status.side_effect = requests.HTTPError(
        'HTTP error',
    )

    with patch(
        'controllcenter.repository.reticulum_api.requests.get',
        return_value=response,
    ):
        with pytest.raises(requests.HTTPError):
            bridge._http_get(endpoint, [], ExampleResponse)


def test_http_post_calls_correct_url_and_sends_data(
    bridge,
    response,
):
    endpoint = Mock(spec=ReticulumBridgeEndpoints.telemetry)
    data = {'status': 'created'}
    expected_model = ExampleResponse
    expected_result = ExampleResponse(status='ok')

    with (
        patch(
            'controllcenter.repository.reticulum_api.requests.post',
            return_value=response,
        ) as mock_post,
        patch.object(
            bridge,
            '_build_url',
            return_value='https://example.invalid/test',
        ) as mock_build_url,
        patch.object(
            bridge,
            '_cast_response',
            return_value=expected_result,
        ) as mock_cast,
    ):
        result = bridge._http_post(
            endpoint,
            [],
            expected_model,
            data,
        )

    mock_build_url.assert_called_once_with(endpoint, [])
    mock_post.assert_called_once_with(
        'https://example.invalid/test',
        json=data,
    )
    mock_cast.assert_called_once_with(response, expected_model)
    assert result is expected_result


def test_http_post_propagates_http_error(bridge, response):
    endpoint = Mock(spec=ReticulumBridgeEndpoints.telemetry)
    endpoint.value = 'telemetry'

    response.raise_for_status.side_effect = requests.HTTPError(
        'HTTP error',
    )

    with patch(
        'controllcenter.repository.reticulum_api.requests.post',
        return_value=response,
    ) as mock_post:
        with pytest.raises(requests.HTTPError):
            bridge._http_post(
                endpoint,
                [],
                ExampleResponse,
                {'status': 'created'},
            )

    mock_post.assert_called_once_with(
        'https://example.invalid/api/telemetry',
        json={'status': 'created'},
    )


def test_build_url_rejects_missing_params(bridge):
    endpoint = Mock(spec=ReticulumBridgeEndpoints.telemetry)
    endpoint.value = 'devices/{}/telemetry/{}'

    with pytest.raises(ValueError):
        bridge._build_url(endpoint, ['device-42'])


def test_build_url_rejects_extra_params(bridge):
    endpoint = Mock(spec=ReticulumBridgeEndpoints.telemetry)
    endpoint.value = 'telemetry'

    with pytest.raises(ValueError):
        bridge._build_url(endpoint, ['unexpected'])


def test_cast_response_checks_http_status_before_json(
    bridge,
    response,
):
    response.raise_for_status.side_effect = requests.HTTPError(
        'HTTP error',
    )

    with pytest.raises(requests.HTTPError):
        bridge._cast_response(response, ExampleResponse)

    response.json.assert_not_called()
