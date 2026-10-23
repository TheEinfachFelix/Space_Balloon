from __future__ import annotations

from functools import cache

from .config import Settings
from .repository.reticulum_api import ReticulumBridge


@cache
def get_settings() -> Settings:
    return Settings()


@cache
def get_reticulum_bridge() -> ReticulumBridge:
    return ReticulumBridge(get_settings())
