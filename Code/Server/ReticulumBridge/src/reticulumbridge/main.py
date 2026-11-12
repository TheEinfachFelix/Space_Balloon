from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger
from reticulumbridge.dependencies import get_influx_connector
from reticulumbridge.dependencies import get_reticulum_bridge


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan-Kontextmanager: Initialisiert beim Start alle Dienste
    und räumt sie beim Herunterfahren auf.
    """
    logger.info('ReticulumBridge wird gestartet...')

    try:
        # 2. InfluxConnector initialisieren
        app.state.influx_connector = get_influx_connector()

        # 3. ReticulumBridge initialisieren
        app.state.reticulum_bridge = get_reticulum_bridge()

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
