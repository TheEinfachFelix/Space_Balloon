from __future__ import annotations

from pydantic import BaseModel
from pydantic import Field


class ResponseData(BaseModel):
    timestamp: str
    id: int
    success: bool = True
    message: str = ''
    result: dict[str, str | int | float | bool] = Field(
        default_factory=dict,
    )
