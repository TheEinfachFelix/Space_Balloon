from __future__ import annotations

from functools import cache

from reticulumbridge.config import Settings
from reticulumbridge.core import CommandHandler
from reticulumbridge.core import ReticulumBridge
from reticulumbridge.core import ReticulumRouter


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
def get_reticulum_bridge() -> ReticulumBridge:
    return ReticulumBridge()
