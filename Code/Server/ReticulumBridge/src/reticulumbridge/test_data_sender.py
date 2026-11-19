from __future__ import annotations

import asyncio
import random
import threading
from datetime import datetime
from datetime import timezone

from loguru import logger
from reticulumbridge.dependencies import get_reticulum_router
from reticulumbridge.models import TelemetryData, ResponseData


def _run_in_new_loop(node_name: str, interval: float, start_value: float):
    """Startet einen eigenen Event-Loop für den Hintergrund-Thread."""
    asyncio.run(
        _simulate_telemetry_random_walk(
            node_name=node_name, interval=interval, start_value=start_value,
        ),
    )


def simulate_telemetry_random_walk(
    node_name: str = 'test-node',
    interval: float = 1.0,
    start_value: float = 50.0,
):
    """Startet die Telemetrie-Simulation in einem separaten Thread

    mit einem eigenen Event-Loop im Hintergrund.
    """
    # Daemon=True sorgt dafür, dass der Thread automatisch
    # stoppt, wenn das Hauptprogramm beendet wird
    thread = threading.Thread(
        target=_run_in_new_loop,
        args=(node_name, interval, start_value),
        daemon=True,
    )
    thread.start()
    logger.info(
        '--- Telemetrie-Simulation in separatem Loop (Thread)'
        f" für '{node_name}' initialisiert ---",
    )


async def _simulate_telemetry_random_walk(
    node_name: str = 'test-node',
    interval: float = 1.0,
    start_value: float = 50.0,
):
    """Führt den Random Walk für test_field_1 aus und sendet

    regelmäßig Telemetriedaten über den Reticulum Router.
    """
    current_value = start_value

    logger.info(
        '--- Starte Telemetrie-Simulation'
        f" (Random Walk) für '{node_name}' ---",
    )

    try:
        while True:
            # Random Walk Schritt (Zufallsänderung zwischen -2.0 und +2.0)
            step = random.uniform(-2.0, 2.0)
            current_value += step

            # Den Wert im Rahmen von 0 bis 100 halten
            current_value = max(0.0, min(100.0, current_value))

            # Pydantic-Objekt erstellen
            data = TelemetryData(
                timestamp=datetime.now(timezone.utc).isoformat(),
                node_name=node_name,
                test_field_1=round(current_value, 2),
            )

            # Router-Aufruf
            router = get_reticulum_router()
            router.route_message('telemetry', data=data)

            response = ResponseData(
                timestamp=datetime.now(timezone.utc).isoformat(),
                id=random.randint(1, 1000),
                node_name=node_name,
                success=True,
                message='Telemetrie erfolgreich gesendet',
                result={'test_field_1': round(current_value, 2)},
            )  

            router.route_message('response', data=response)

            logger.info(
                f"[{data.timestamp}] Gesendet via Router: {data.model_dump()}",
            )

            # Warten bis zum nächsten Intervall
            await asyncio.sleep(interval)

    except asyncio.CancelledError:
        logger.warning(
            f"--- Telemetrie-Simulation für '{node_name}' gestoppt ---",
        )
