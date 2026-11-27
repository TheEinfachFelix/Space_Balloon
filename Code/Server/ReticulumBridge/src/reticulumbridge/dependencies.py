from __future__ import annotations

from functools import cache

from reticulumbridge.config import Settings
from reticulumbridge.core import CommandHandler
from reticulumbridge.core import ReticulumBridge
from reticulumbridge.core import ReticulumRouter
from reticulumbridge.core.dummy_reticulum_bridge import DummyReticulumBridge
from reticulumbridge.services.influx import InfluxConnector


@cache
def get_settings() -> Settings:
    return Settings()


@cache
def get_reticulum_router() -> ReticulumRouter:
    return ReticulumRouter()


@cache
def get_command_handler() -> CommandHandler:
    handler = CommandHandler()
    get_reticulum_router().register_route(handler)
    return handler


@cache
def get_reticulum_bridge() -> ReticulumBridge | DummyReticulumBridge:
    settings = get_settings()
    bridge_type = (
        DummyReticulumBridge
        if settings.reticulum_bridge.use_dummy_bridge
        else ReticulumBridge
    )
    bridge = bridge_type()
    get_reticulum_router().register_route(bridge)
    return bridge


@cache
def get_influx_connector() -> InfluxConnector:
    connector = InfluxConnector()
    get_reticulum_router().register_route(connector)
    return connector
