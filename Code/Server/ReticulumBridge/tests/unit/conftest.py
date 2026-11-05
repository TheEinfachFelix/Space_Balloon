from __future__ import annotations

from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest
from reticulumbridge.config import APIConfig
from reticulumbridge.config import InfluxDBSharedConfig
from reticulumbridge.config import ReticulumBridgeConfig
from reticulumbridge.config import Settings


@pytest.fixture
def mock_settings():
    """Vollständig ausgestattete
    Mock-Settings für alle Konfigurationsmodelle."""
    with patch('reticulumbridge.dependencies.get_settings') as mock_get:
        settings = MagicMock(spec=Settings)

        # InfluxDB Shared Config mocken
        settings.influxdb_shared_config = InfluxDBSharedConfig(
            url='http://localhost:8086',
            org='test-org',
            bucket='test-bucket',
        )

        # Reticulum Bridge Config mocken
        settings.reticulum_bridge = ReticulumBridgeConfig(
            influxdb_token='test-token-123',
            logging_level='INFO',
            api=APIConfig(
                host='127.0.0.1',
                port=8000,
            ),
            reticulum_timeout_s=0.2,  # Standard-Test-Timeout
        )

        mock_get.return_value = settings
        yield settings


@pytest.fixture
def mock_reticulum_bridge():
    """Zentrale Fixture zum Mocken der Reticulum Bridge."""
    with (
        patch('reticulumbridge.dependencies.get_reticulum_bridge')
        as mock_get,
    ):
        bridge = MagicMock()
        bridge.sendMsg = AsyncMock()
        mock_get.return_value = bridge
        yield bridge
