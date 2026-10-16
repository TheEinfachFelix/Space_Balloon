from __future__ import annotations

from functools import lru_cache

from .config import Settings


@lru_cache
def get_settings() -> Settings:
    return Settings()
