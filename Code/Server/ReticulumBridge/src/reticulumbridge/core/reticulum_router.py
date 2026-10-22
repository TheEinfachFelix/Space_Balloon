from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable
from typing import TypeVar

from loguru import logger

Handler = Callable[..., None]
F = TypeVar('F', bound=Handler)


def reticulum_response_route(event_name: str) -> Callable[[F], F]:
    """Markiert eine Methode als Handler für ein Event."""

    def decorator(func: F) -> F:
        setattr(func, '__route_event__', event_name)
        return func

    return decorator


class ReticulumRouter:
    def __init__(self) -> None:
        self._observers: defaultdict[str, list[Handler]] = defaultdict(list)
        logger.debug('ReticulumRouter initialized')

    def register(self, event_name: str, handler: Handler) -> None:
        if handler in self._observers[event_name]:
            logger.debug('Handler already registered: {}', event_name)
            return

        self._observers[event_name].append(handler)
        logger.debug('Handler registered: {}', event_name)

    def register_route(self, handler: object) -> None:
        """Registriert alle dekorierten Methoden eines Objekts."""
        registered = 0

        for name in dir(handler):
            method = getattr(handler, name)
            event_name = getattr(method, '__route_event__', None)

            if isinstance(event_name, str) and callable(method):
                before = len(self._observers[event_name])
                self.register(event_name, method)
                registered += len(self._observers[event_name]) > before

        logger.debug(
            'Registered {} routes for {}',
            registered,
            type(handler).__name__,
        )

    def route_message(self, event_name: str, data: object) -> None:
        handlers = self._observers.get(event_name, [])

        if not handlers:
            logger.warning('No handlers registered for event: {}', event_name)
            return

        logger.debug(
            "Routing event '{}' to {} handler(s)",
            event_name,
            len(handlers),
        )

        for func in handlers:
            try:
                func(data)
            except Exception:
                logger.exception('Handler failed for event: {}', event_name)
                raise
