from __future__ import annotations

from typing import Literal

from pydantic import BaseModel
from pydantic import Field


class CommandData(BaseModel):
    timestamp: str
    id: int
    node_name: str
    command: Literal['ping', 'get_status', 'set_mode'] = 'ping'
    parameters: dict[str, str | int | float | bool] = Field(
        default_factory=dict,
    )
