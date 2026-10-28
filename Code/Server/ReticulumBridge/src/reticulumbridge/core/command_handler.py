from __future__ import annotations

import asyncio

from loguru import logger
from reticulumbridge.core.reticulum_router import reticulum_response_route
from reticulumbridge.models import CommandData
from reticulumbridge.models import ResponseData


class CommandHandler:
    def __init__(self):
        logger.info('CommandHandler initializing...')
        self._pending_commands: dict[int, asyncio.Future] = {}

        from reticulumbridge.dependencies import get_settings
        settings = get_settings()
        self.timeout_s = settings.reticulum_bridge.reticulum_timeout_s

        logger.success('CommandHandler initialized successfully.')

    async def send_command(self, command: CommandData) -> ResponseData:
        logger.info(f"Sending command: {command}")

        loop = asyncio.get_running_loop()
        future = loop.create_future()

        # Command registrieren
        self._pending_commands[command.id] = future

        try:
            # Senden an Reticulum
            from reticulumbridge.dependencies import get_reticulum_bridge
            bridge = get_reticulum_bridge()
            await bridge.sendMsg(command)

            # Warten auf Antwort mit konfigurierbarem Timeout
            response = await asyncio.wait_for(future, timeout=self.timeout_s)

            logger.success(f"Command {command.id} successfully completed.")
            return response

        except TimeoutError:
            logger.error(
                f"Timeout ({self.timeout_s}s) reached "
                'while waiting for command: {command.id}',
            )
            raise TimeoutError(f"Command {command.id} timed out.")
        except Exception as e:
            logger.error(f"Error while sending command {command.id}: {e}")
            raise
        finally:
            # Cleanup der Registrierung
            self._pending_commands.pop(command.id, None)

    @reticulum_response_route('response')
    def _handle_response(self, response: ResponseData) -> None:
        logger.info(
            f"Handling incoming response for command ID: {response.id}",
        )

        future = self._pending_commands.get(response.id)
        if future and not future.done():
            #  Setzt das Ergebnis des Futures, wodurch send_command aufwacht
            future.set_result(response)
            logger.success(
                'Response successfully assigned to '
                f'future for command: {response.id}',
            )
        else:
            logger.warning(
                'Received response for unknown or '
                f'already completed command: {response.id}',
            )
