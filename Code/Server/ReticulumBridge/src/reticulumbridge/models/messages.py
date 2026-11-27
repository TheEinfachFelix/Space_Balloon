from __future__ import annotations

from typing import Annotated
from typing import Literal

from pydantic import BaseModel
from pydantic import Field

from .command import CommandData
from .response import ResponseData
from .telemetry import TelemetryData

MessagePayload = CommandData | ResponseData | TelemetryData


class CommandMessage(BaseModel):
    type: Literal['command'] = 'command'
    data: CommandData


class ResponseMessage(BaseModel):
    type: Literal['response'] = 'response'
    data: ResponseData


class TelemetryMessage(BaseModel):
    type: Literal['telemetry'] = 'telemetry'
    data: TelemetryData


ReticulumMessage = Annotated[
    CommandMessage | ResponseMessage | TelemetryMessage,
    Field(discriminator='type'),
]
