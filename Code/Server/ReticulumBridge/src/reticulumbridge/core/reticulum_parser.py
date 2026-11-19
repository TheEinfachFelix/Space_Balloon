from __future__ import annotations

from pydantic import BaseModel
from pydantic import TypeAdapter
from reticulumbridge.models import CommandData
from reticulumbridge.models import CommandMessage
from reticulumbridge.models import MessagePayload
from reticulumbridge.models import ResponseData
from reticulumbridge.models import ResponseMessage
from reticulumbridge.models import ReticulumMessage
from reticulumbridge.models import TelemetryData
from reticulumbridge.models import TelemetryMessage

_MESSAGE_TYPES: dict[type[BaseModel], type[BaseModel]] = {
    CommandData: CommandMessage,
    ResponseData: ResponseMessage,
    TelemetryData: TelemetryMessage,
}
_MESSAGE_ADAPTER = TypeAdapter(ReticulumMessage)


def compress(data: MessagePayload) -> str:
    message_model = _MESSAGE_TYPES.get(type(data))
    if message_model is None:
        raise TypeError(f'Unsupported message model: {type(data).__name__}')

    return message_model(data=data).model_dump_json()


def decompress(data: str) -> MessagePayload:
    return typeify(data)


def typeify(data: str) -> MessagePayload:
    """Parse a JSON message envelope into its corresponding Pydantic model."""
    message = _MESSAGE_ADAPTER.validate_json(data)
    return message.data
