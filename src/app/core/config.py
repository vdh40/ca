import os

from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class ExchangesConfig(BaseModel):
    coingecko_url: str
    binance_url: str


class DbConfig(BaseModel):
    url: PostgresDsn
    schema_name: str = "public"


class Config(BaseSettings):
    api_prefix: str = "/api"

    host: str = "0.0.0.0"
    port: int = 5000

    db: DbConfig
    exchanges: ExchangesConfig


class DevConfig(Config):
    model_config = SettingsConfigDict(env_file=".env", env_nested_delimiter="__")


class MigrationConfig(Config):
    model_config = SettingsConfigDict(env_file=".env.alembic", env_nested_delimiter="__")


def get_config() -> Config:
    env_type = os.getenv("ENV_TYPE")

    config_class: type[BaseSettings] | None = None

    if env_type == "alembic":
        config_class = MigrationConfig
    else:
        config_class = DevConfig

    return config_class()


config = get_config()
