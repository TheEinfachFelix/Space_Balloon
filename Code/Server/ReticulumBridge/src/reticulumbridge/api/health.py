from __future__ import annotations

from fastapi import APIRouter
from reticulumbridge.models import CommandData
from reticulumbridge.dependencies import get_command_handler
import datetime

router = APIRouter()


@router.get('/health')
def health_check():
    return {'status': 'healthy', 'service': 'reticulum-bridge'}

@router.post("/command/reboot")
async def reboot():
    command = CommandData(
        timestamp=datetime.datetime.now().isoformat(), 
        id=1, 
        node_name="default", 
        command="reboot", 
        parameters={}
    )
    handler = get_command_handler()
    return await handler.send_command(command)