from __future__ import annotations

from loguru import logger
from reticulumbridge.core.reticulum_router import reticulum_response_route


class CommandHandler:
    def __init__(self):
        logger.info('CommandHandler initializing...')

        logger.success('CommandHandler initialized successfully.')

    # str ist der falsche datentyp, es muss durch das model erstet werden.
    async def send_command(self, command: str):
        logger.info(f"Sending command: {command}")

        logger.success(f"Command sent successfully: {command}")

    @reticulum_response_route('response')  # response muss angepasst werden
    # str ist der falsche datentyp, es muss durch das model erstet werden.
    def handle_response(self, response: str):
        logger.info(f"Handling response: {response}")

        logger.success(f"Response handled successfully: {response}")
