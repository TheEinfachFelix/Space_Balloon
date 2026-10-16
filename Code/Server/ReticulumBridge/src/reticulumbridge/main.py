from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger
from reticulumbridge.core.reticulum import ReticulumBridge
from reticulumbridge.dependencies import get_settings
from reticulumbridge.services.influx import InfluxConfig
from reticulumbridge.services.influx import InfluxConnector


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan-Kontextmanager: Initialisiert beim Start alle Dienste
    und räumt sie beim Herunterfahren auf.
    """
    settings = get_settings()

    logger.info('ReticulumBridge wird gestartet...')

    try:
        # 2. InfluxConnector initialisieren
        influx_config = InfluxConfig(
            url=settings.influxdb_shared_config.url,
            token=settings.reticulum_bridge.influxdb_token,
            org=settings.influxdb_shared_config.org,
            bucket=settings.influxdb_shared_config.bucket,
        )
        app.state.influx_connector = InfluxConnector(influx_config)

        # 3. ReticulumBridge initialisieren
        app.state.reticulum_bridge = ReticulumBridge()

        logger.success('Alle Hintergrunddienste erfolgreich gestartet.')
    except Exception as e:
        logger.critical(f"Kritischer Fehler beim Starten der Services: {e}")
        raise e

    yield  # Die FastAPI-App läuft

    logger.info('ReticulumBridge wird heruntergefahren...')

    # Referenzen im App-State löschen (löst __del__ / Cleanup aus)
    app.state.reticulum_bridge = None
    app.state.influx_connector = None

    logger.success('ReticulumBridge erfolgreich beendet.')
