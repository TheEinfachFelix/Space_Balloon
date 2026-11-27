from __future__ import annotations

from pydantic import Field

from .base import BaseData


class ResponseData(BaseData):
    timestamp: str
    id: int
    success: bool = True
    message: str = ''
    result: dict[str, str | int | float | bool] = Field(
        default_factory=dict,
    )
