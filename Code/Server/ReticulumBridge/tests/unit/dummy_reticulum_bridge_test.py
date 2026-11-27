from __future__ import annotations

import asyncio
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest
from reticulumbridge.core.command_handler import CommandHandler
from reticulumbridge.core.dummy_reticulum_bridge import DummyReticulumBridge
from reticulumbridge.core.reticulum_router import ReticulumRouter
from reticulumbridge.dependencies import get_reticulum_bridge
from reticulumbridge.dependencies import get_reticulum_router
from reticulumbridge.models import CommandData
from reticulumbridge.models import ResponseData


@pytest.mark.asyncio
async def test_send_msg_returns_successful_response_to_command_handler(
    mock_settings,
    mock_influx_connector,
):
    command = CommandData(
        id=42,
        timestamp='test-timestamp',
        node_name='test-node',
        command='set_mode',
        parameters={'mode': 'safe'},
    )
    mock_influx_connector.generate_id.return_value = command.id
    router = ReticulumRouter()
    router.register(
        'send',
        lambda data: asyncio.create_task(bridge.sendMsg(data)),
    )
    handler = CommandHandler()
    assert (
        handler.timeout_s
        == mock_settings.reticulum_bridge.reticulum.timeout_s
    )
    router.register_route(handler)
    bridge = DummyReticulumBridge()

    with (
        patch(
            'reticulumbridge.dependencies.get_reticulum_router',
            return_value=router,
        ),
        patch(
            'reticulumbridge.dependencies.get_reticulum_bridge',
            return_value=bridge,
        ),
    ):
        response = await handler.send_command(command)

    assert isinstance(response, ResponseData)
    assert response.id == command.id
    assert response.timestamp == command.timestamp
    assert response.node_name == command.node_name
    assert response.success is True
    assert response.result == command.parameters
    mock_influx_connector.generate_id.assert_called_once_with()


@pytest.mark.parametrize(
    'use_dummy_bridge',
    [True, False],
)
def test_bridge_dependency_uses_configured_implementation(
    mock_settings,
    use_dummy_bridge,
):
    mock_settings.reticulum_bridge.use_dummy_bridge = use_dummy_bridge
    get_reticulum_bridge.cache_clear()
    get_reticulum_router.cache_clear()

    try:
        with patch(
            'reticulumbridge.dependencies.ReticulumBridge',
            return_value=MagicMock(),
        ) as real_bridge:
            bridge = get_reticulum_bridge()

        if use_dummy_bridge:
            real_bridge.assert_not_called()
            assert isinstance(bridge, DummyReticulumBridge)
        else:
            real_bridge.assert_called_once_with()
            assert bridge is real_bridge.return_value
    finally:
        get_reticulum_bridge.cache_clear()
        get_reticulum_router.cache_clear()
