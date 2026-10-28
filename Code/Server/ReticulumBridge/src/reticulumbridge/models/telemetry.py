from __future__ import annotations

from pydantic import BaseModel


class TelemetryData(BaseModel):
    timestamp: str
    # Hier können weitere Felder für Telemetriedaten hinzugefügt werden
