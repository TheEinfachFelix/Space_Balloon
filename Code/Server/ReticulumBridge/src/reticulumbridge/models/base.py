from __future__ import annotations

from pydantic import BaseModel


class BaseData(BaseModel):
    timestamp: str
    id: int
    node_name: str
