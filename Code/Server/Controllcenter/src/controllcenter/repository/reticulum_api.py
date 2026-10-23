from __future__ import annotations

import requests
from controllcenter.config import Settings
from controllcenter.models import TelemetryData
from controllcenter.repository import ReticulumBridgeEndpoints
from pydantic import BaseModel


class ReticulumBridge:
    def __init__(self, config: Settings):
        self.config = config
        self.api_url = config.controllcenter_config.reticulum_api_url

    # ----------------- Utility Functions -----------------

    def _build_url(
            self,
            endpoint: ReticulumBridgeEndpoints,
            params: list[str],
    ) -> str:
        url = f"{self.api_url}/{endpoint.value}"
        if len(params) != url.count('{}'):
            raise ValueError(
                f"Expected {url.count('{}')} parameters, got {len(params)}",
            )
        for i in params:
            url = url.replace('{}', i, 1)
        return url

    def _cast_response(
            self,
            response: requests.Response,
            model: type[BaseModel],
    ) -> BaseModel:
        response.raise_for_status()
        json_data = response.json()
        return model.model_validate(json_data)

    def _http_get(
            self,
            endpoint: ReticulumBridgeEndpoints,
            params: list[str],
            model: type[BaseModel],
    ) -> BaseModel:
        url = self._build_url(endpoint, params)
        response = requests.get(url)
        return self._cast_response(response, model)

    def _http_post(
            self,
            endpoint: ReticulumBridgeEndpoints,
            params: list[str],
            model: type[BaseModel],
            data: dict,
    ) -> BaseModel:
        url = self._build_url(endpoint, params)
        response = requests.post(url, json=data)
        return self._cast_response(response, model)

    # ----------------- API Functions -----------------

    def get_telemetry(self) -> TelemetryData:
        return self._http_get(
            ReticulumBridgeEndpoints.telemetry,
            [],
            TelemetryData,
        )
