# tests/conftest.py
from __future__ import annotations

from unittest.mock import Mock

import pytest
import requests
from controllcenter.config import Settings
from controllcenter.repository import ReticulumBridge
from pydantic import BaseModel


class ExampleResponse(BaseModel):
    status: str


@pytest.fixture
def config() -> Settings:
    config = Mock(spec=Settings)
    config.controllcenter_config = Mock()
    config.controllcenter_config.reticulum_api_url = (
        'https://example.invalid/api'
    )
    return config


@pytest.fixture
def bridge(config: Settings) -> ReticulumBridge:
    """Neue Bridge-Instanz pro Test."""
    return ReticulumBridge(config)


@pytest.fixture
def response() -> Mock:
    """Erfolgreiche HTTP-Response mit JSON-Inhalt."""
    response = Mock(spec=requests.Response)
    response.json.return_value = {'status': 'ok'}
    response.raise_for_status.return_value = None
    return response
