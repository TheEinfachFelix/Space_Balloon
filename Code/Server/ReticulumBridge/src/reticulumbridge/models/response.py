from __future__ import annotations

from pydantic import BaseModel


class ResponseData(BaseModel):
    timestamp: str
    id: int
    # Hier können weitere Felder für Telemetriedaten hinzugefügt werden
