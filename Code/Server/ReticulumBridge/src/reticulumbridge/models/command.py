from __future__ import annotations

from typing import Literal

from pydantic import Field

from .base import BaseData


class CommandData(BaseData):
    timestamp: str = ''
    id: int = -1
    command: Literal['ping', 'get_status', 'set_mode', 'reboot'] = 'ping'
    parameters: dict[str, str | int | float | bool] = Field(
        default_factory=dict,
    )
