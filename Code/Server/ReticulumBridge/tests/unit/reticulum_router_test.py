from __future__ import annotations

import pytest
from reticulumbridge.core.reticulum_router import reticulum_response_route
from reticulumbridge.core.reticulum_router import ReticulumRouter


class TestHandler:
    def __init__(self):
        self.received = []

    @reticulum_response_route('response')
    def handle_response(self, data):
        self.received.append(data)


def test_register_route_registers_decorated_handler():
    router = ReticulumRouter()
    handler = TestHandler()

    router.register_route(handler)

    assert len(router._observers['response']) == 1


def test_route_message_calls_registered_handler():
    router = ReticulumRouter()
    handler = TestHandler()
    router.register_route(handler)

    router.route_message('response', {'status': 'ok'})

    assert len(handler.received) == 1


def test_route_message_forwards_correct_data():
    router = ReticulumRouter()
    handler = TestHandler()
    router.register_route(handler)
    payload = {'status': 'ok', 'sequence': 42}

    router.route_message('response', payload)

    assert handler.received[0] == payload
    assert handler.received[0] is payload


def test_route_message_calls_multiple_handlers():
    router = ReticulumRouter()
    first = TestHandler()
    second = TestHandler()

    router.register_route(first)
    router.register_route(second)

    payload = {'status': 'ok'}
    router.route_message('response', payload)

    assert first.received == [payload]
    assert second.received == [payload]


def test_unknown_event_does_not_raise():
    """Unbekannte Events dürfen keinen Fehler auslösen."""
    router = ReticulumRouter()

    router.route_message('unknown', {'value': 1})


def test_unknown_event_does_not_call_other_handlers():
    """Ein Handler darf nur auf sein registriertes Event reagieren."""
    router = ReticulumRouter()
    handler = TestHandler()
    router.register_route(handler)

    router.route_message('unknown', {'value': 1})

    assert handler.received == []


@pytest.mark.parametrize(
    'payload',
    [
        None,
        {},
        [],
        '',
        0,
        False,
    ],
)
def test_route_message_forwards_empty_or_falsy_payloads(payload):
    """Auch None und andere falsy Werte müssen weitergereicht werden."""
    router = ReticulumRouter()
    handler = TestHandler()
    router.register_route(handler)

    router.route_message('response', payload)

    assert len(handler.received) == 1
    assert handler.received[0] is payload


def test_handler_receives_multiple_messages_in_order():
    router = ReticulumRouter()
    handler = TestHandler()
    router.register_route(handler)

    messages = [{'id': 1}, {'id': 2}, {'id': 3}]

    for message in messages:
        router.route_message('response', message)

    assert handler.received == messages


def test_events_are_isolated():
    """Ein Handler für response darf keine anderen Events empfangen."""

    class MultiEventHandler:
        def __init__(self):
            self.responses = []
            self.errors = []

        @reticulum_response_route('response')
        def handle_response(self, data):
            self.responses.append(data)

        @reticulum_response_route('error')
        def handle_error(self, data):
            self.errors.append(data)

    router = ReticulumRouter()
    handler = MultiEventHandler()
    router.register_route(handler)

    router.route_message('response', 'success')

    assert handler.responses == ['success']
    assert handler.errors == []


def test_only_decorated_methods_are_registered():
    """Normale Methoden dürfen nicht automatisch registriert werden."""

    class MixedHandler:
        def __init__(self):
            self.called = False

        def ordinary_method(self, data):
            self.called = True

        @reticulum_response_route('response')
        def handle_response(self, data):
            self.called = True

    router = ReticulumRouter()
    handler = MixedHandler()
    router.register_route(handler)

    assert len(router._observers['response']) == 1

    router.route_message('response', {})

    assert handler.called is True


def test_same_handler_registered_twice_is_not_duplicated():
    """Eine wiederholte Registrierung soll keine doppelten Aufrufe erzeugen."""
    router = ReticulumRouter()
    handler = TestHandler()

    router.register_route(handler)
    router.register_route(handler)

    router.route_message('response', {'id': 1})

    assert handler.received == [{'id': 1}]


def test_multiple_handlers_are_called_in_registration_order():
    """Handler werden in der Reihenfolge ihrer Registrierung aufgerufen."""
    calls = []

    class OrderedHandler:
        def __init__(self, name):
            self.name = name

        @reticulum_response_route('response')
        def handle(self, data):
            calls.append(self.name)

    router = ReticulumRouter()
    router.register_route(OrderedHandler('first'))
    router.register_route(OrderedHandler('second'))
    router.register_route(OrderedHandler('third'))

    router.route_message('response', {})

    assert calls == ['first', 'second', 'third']


def test_handler_can_be_registered_on_multiple_router_instances():
    """Die Registrierung auf einem Router beeinflusst keinen anderen."""
    first_router = ReticulumRouter()
    second_router = ReticulumRouter()
    handler = TestHandler()

    first_router.register_route(handler)

    first_router.route_message('response', 'first')
    second_router.route_message('response', 'second')

    assert handler.received == ['first']


def test_handler_exception_is_propagated():
    """Fehler im Handler werden nicht stillschweigend verschluckt."""

    class FailingHandler:
        @reticulum_response_route('response')
        def handle(self, data):
            raise ValueError('Handler failed')

    router = ReticulumRouter()
    router.register_route(FailingHandler())

    with pytest.raises(ValueError, match='Handler failed'):
        router.route_message('response', {})
