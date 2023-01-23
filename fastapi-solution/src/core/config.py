from pathlib import Path

from logging import config as logging_config
from pydantic import BaseSettings, Field

from core.logger import LOGGING


class Settings(BaseSettings):
    redis_host: str = Field(..., env='REDIS_HOST')
    redis_port: int = Field(..., env='REDIS_PORT')
    project_name: str = Field(..., env='PROJECT_NAME')
    elastic_host: str = Field(..., env='ELASTIC_HOST')
    elastic_port: int = Field(..., env='ELASTIC_PORT')
    redis_cache_expire_seconds: int = Field(..., env='REDIS_CACHE_EXPIRE_SECONDS')

    class Config:
        env_file = str(Path(__file__).parents[3]) + '/.env'
        env_file_encoding = 'utf-8'


settings = Settings()
logging_config.dictConfig(LOGGING)
