from __future__ import annotations

from pydantic import BaseModel


class TelemetryData(BaseModel):
    timestamp: str
    node_name: str
    test_field_1: float
    # Hier können weitere Felder für Telemetriedaten hinzugefügt werden
