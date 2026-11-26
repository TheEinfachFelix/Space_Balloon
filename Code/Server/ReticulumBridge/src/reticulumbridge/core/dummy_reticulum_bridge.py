from __future__ import annotations

from loguru import logger
from reticulumbridge.models import CommandData
from reticulumbridge.models import ResponseData


class DummyReticulumBridge:
    def __init__(self) -> None:
        logger.info('DummyReticulumBridge initialized')

    async def sendMsg(self, data: CommandData) -> None:
        response = ResponseData(
            id=data.id,
            timestamp=data.timestamp,
            node_name=data.node_name,
            success=True,
            message=f'Dummy response for command {data.command}',
            result=data.parameters.copy(),
        )

        from reticulumbridge.dependencies import get_reticulum_router

        get_reticulum_router().route_message('response', response)
