from __future__ import annotations

from loguru import logger
from reticulumbridge.core.reticulum_router import reticulum_response_route
from reticulumbridge.models import CommandData
from reticulumbridge.models import ResponseData


class CommandHandler:
    def __init__(self):
        logger.info('CommandHandler initializing...')

        logger.success('CommandHandler initialized successfully.')

    async def send_command(self, command: CommandData) -> ResponseData:
        logger.info(f"Sending command: {command}")

        logger.success(f"Command sent successfully: {command}")
        return command

    @reticulum_response_route('response')
    def handle_response(self, response: ResponseData) -> None:
        logger.info(f"Handling response: {response}")

        logger.success(f"Response handled successfully: {response}")
