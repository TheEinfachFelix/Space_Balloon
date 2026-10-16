from __future__ import annotations

from loguru import logger


def main() -> None:

    # Beispiel für den Start der Bridge
    logger.info('ReticulumBridge wird gestartet...')
    logger.debug('Lausche auf TCP-Interface für Bodenstation...')

    try:
        # Eingehendes Paket empfangen
        logger.success(
            'Paket von Bodenstation erfolgreich empfangen und validiert.',
        )
    except Exception as e:
        logger.error(f"Fehler beim Verarbeiten des Pakets: {e}")
