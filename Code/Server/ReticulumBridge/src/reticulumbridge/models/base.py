from __future__ import annotations

from pydantic import BaseModel


class BaseData(BaseModel):
    node_name: str
