from __future__ import annotations

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic_settings import BaseSettings
from pydantic_settings import PydanticBaseSettingsSource
from pydantic_settings import SettingsConfigDict
from pydantic_settings import YamlConfigSettingsSource


class StrictModel(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
        strict=True,
    )


class InfluxDBSharedConfig(StrictModel):
    url: str
    org: str
    bucket: str


class ControllCenterConfig(StrictModel):
    reticulum_api_url: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        yaml_file='config.yml',
        yaml_file_encoding='utf-8',
        extra='ignore',
    )

    influxdb_shared_config: InfluxDBSharedConfig
    controllcenter_config: ControllCenterConfig

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            YamlConfigSettingsSource(settings_cls),
            file_secret_settings,
        )
