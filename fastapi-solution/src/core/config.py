import os

from logging import config as logging_config
from pydantic import BaseSettings, Field

from core.logger import LOGGING


# class Settings(BaseSettings):
#     redis_host: str = Field(..., env='REDIS_HOST')
#     redis_port: int = Field(..., env='REDIS_PORT')
#     project_name: str = Field(..., env='PROJECT_NAME')
#     elastic_host: str = Field(..., env='ELASTIC_HOST')
#     elastic_port: int = Field(..., env='ELASTIC_PORT')
#     base_dir: str = Field(..., env='BASE_DIR')

#     class Congif:
#         env_file = '.env'

# setting = Settings()

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)

# Название проекта. Используется в Swagger-документации
PROJECT_NAME = os.getenv('PROJECT_NAME', 'movies')

# Настройки Redis
REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))

# Настройки Elasticsearch
ELASTIC_HOST = os.getenv('ELASTIC_HOST', '127.0.0.1')
ELASTIC_PORT = int(os.getenv('ELASTIC_PORT', 9200))

# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

REDIS_CACHE_EXPIRE_SECONDS = 60 * 5  # 5 минут
