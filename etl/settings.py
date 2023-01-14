"""Module with settings."""
import os
from pydantic import BaseSettings, Field


class PostgresSettings(BaseSettings):
    dbname: str = os.environ.get('POSTGRES_DB')
    user: str = os.environ.get('POSTGRES_USER')
    password: str = os.environ.get('POSTGRES_PASSWORD')
    host: str = os.environ.get('POSTGRES_HOST')
    port: int = os.environ.get('POSTGRES_PORT')
    options: str = os.environ.get('DB_OPTIONS')


class Settings(BaseSettings):
    last_state_key: str = os.environ.get('ETL_STATE_KEY')
    state_file_path: str = os.environ.get('ETL_STATE_STORAGE')
    dsn: PostgresSettings = PostgresSettings()
    batch_size: int = os.environ.get('CHUNK_SIZE')
    es_host: str = os.environ.get('ES_URL')
    es_index_name: str = os.environ.get('ES_INDEX_NAME')
    offset_counter: int = 0


settings = Settings()
