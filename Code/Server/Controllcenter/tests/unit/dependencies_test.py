# tests/test_dependencies.py
from __future__ import annotations

from unittest.mock import patch

import pytest
from controllcenter.config import Settings
from controllcenter.dependencies import get_reticulum_bridge
from controllcenter.dependencies import get_settings


@pytest.fixture(autouse=True)
def clear_dependency_caches():
    """Verhindert, dass Testergebnisse voneinander abhängen."""
    get_reticulum_bridge.cache_clear()
    get_settings.cache_clear()

    yield

    get_reticulum_bridge.cache_clear()
    get_settings.cache_clear()


def test_get_settings_creates_settings_once():
    with patch(
        'controllcenter.dependencies.Settings',
        autospec=True,
    ) as settings_class:
        first = get_settings()
        second = get_settings()

    assert isinstance(first, Settings)
    assert first is second
    settings_class.assert_called_once_with()


def test_get_reticulum_bridge_creates_bridge_once():
    with (
        patch(
            'controllcenter.dependencies.get_settings',
            autospec=True,
        ) as settings_dependency,
        patch(
            'controllcenter.dependencies.ReticulumBridge',
            autospec=True,
        ) as bridge_class,
    ):
        settings = settings_dependency.return_value

        first = get_reticulum_bridge()
        second = get_reticulum_bridge()

    assert first is second
    bridge_class.assert_called_once_with(settings)
    settings_dependency.assert_called_once_with()


def test_bridge_uses_cached_settings():
    with (
        patch(
            'controllcenter.dependencies.Settings',
            autospec=True,
        ) as settings_class,
        patch(
            'controllcenter.dependencies.ReticulumBridge',
            autospec=True,
        ) as bridge_class,
    ):
        first = get_reticulum_bridge()
        second = get_reticulum_bridge()

    assert first is second
    settings_class.assert_called_once_with()
    bridge_class.assert_called_once_with(
        settings_class.return_value,
    )
