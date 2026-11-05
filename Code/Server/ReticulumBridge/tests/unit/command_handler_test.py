from __future__ import annotations

import asyncio

import pytest
from reticulumbridge.dependencies import get_command_handler
from reticulumbridge.models import CommandData
from reticulumbridge.models import ResponseData


def test_command_handler_initialization(mock_settings):
    """Test 1: Initialisierung lädt
    den Timeout korrekt aus den Settings."""
    handler = get_command_handler()
    assert handler.timeout_s == 0.2
    assert isinstance(handler._pending_commands, dict)
    assert len(handler._pending_commands) == 0


def test_response_route_decorator(mock_settings):
    """Test 2: Der Callback-Handler
    ist korrekt mit dem Router-Decorator versehen."""
    handler = get_command_handler()

    # Prüfen, ob das Dekorator-Attribut __route_event__ vorhanden ist
    assert hasattr(handler._handle_response, '__route_event__')
    assert handler._handle_response.__route_event__ == 'response'


@pytest.mark.asyncio
async def test_handle_response_resolves_future(mock_settings):
    """Test 3: Der Response-Handler weist
    das Ergebnis dem entsprechenden Future zu."""
    handler = get_command_handler()

    # Ein Future für einen Befehl manuell registrieren
    loop = asyncio.get_running_loop()
    future = loop.create_future()
    command_id = 1535
    handler._pending_commands[command_id] = future

    # Eine Antwort simulieren
    response = ResponseData(id=command_id, timestamp='asdfg')
    handler._handle_response(response)

    # Prüfen, ob das Future aufgelöst wurde
    assert future.done()
    result = await future
    assert result.id == command_id
    assert result.timestamp == 'asdfg'


@pytest.mark.asyncio
async def test_send_command_success(mock_settings, mock_reticulum_bridge):
    """Test 4: send_command wartet
    erfolgreich auf die Antwort und gibt sie zurück."""
    handler = get_command_handler()
    command = CommandData(id=123456, timestamp='asdfgh')

    async def simulate_async_response():
        await asyncio.sleep(0.05)
        response = ResponseData(id=123456, timestamp='asdfgh')
        handler._handle_response(response)

    asyncio.create_task(simulate_async_response())

    response = await handler.send_command(command)

    mock_reticulum_bridge.sendMsg.assert_awaited_once_with(command)
    assert response.id == 123456
    assert response.timestamp == 'asdfgh'


@pytest.mark.asyncio
async def test_send_command_timeout(
    mock_settings,
    mock_reticulum_bridge,
):
    """Test 5: send_command bricht mit Timeout ab und
    bereinigt den Pending-Eintrag."""
    handler = get_command_handler()
    command = CommandData(id=1007, timestamp='asdfghj')

    with pytest.raises((asyncio.TimeoutError, TimeoutError)):
        await handler.send_command(command)

    # Prüfen, ob der Eintrag trotz Timeout aufgeräumt wurde
    assert 1007 not in handler._pending_commands


@pytest.mark.asyncio
async def test_send_command_cleans_up_pending_on_success(
    mock_settings,
    mock_reticulum_bridge,
):
    """Test 6: Sicherstellen, dass _pending_commands
    nach erfolgreichem Befehl bereinigt wird."""
    handler = get_command_handler()
    command = CommandData(id=999, timestamp='cleanup-test')

    async def simulate_async_response():
        await asyncio.sleep(0.02)
        handler._handle_response(
            ResponseData(
                id=999, timestamp='cleanup-test',
            ),
        )

    asyncio.create_task(simulate_async_response())

    await handler.send_command(command)

    # Prüfen, ob das Dict für diese ID wieder leer/gereinigt ist
    assert 999 not in handler._pending_commands


def test_handle_response_unknown_command_id(mock_settings):
    """Test 7: Eine Antwort für eine unbekannte ID wirft
    keinen Fehler und loggt eine Warnung."""
    handler = get_command_handler()

    # Antwort für eine ID senden, die nie registriert wurde
    response = ResponseData(id=404, timestamp='orphan')

    # Sollte ohne Exception durchlaufen
    handler._handle_response(response)
    assert 404 not in handler._pending_commands
