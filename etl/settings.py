"""Module with settings."""
import os
from pydantic import BaseSettings, Field


class PostgresSettings(BaseSettings):
    dbname: str = os.environ.get('POSTGRES_DB', 'movies_database')
    user: str = 'app'
    password: str = os.environ.get('POSTGRES_PASSWORD', '95463b11287')
    host: str = os.environ.get('POSTGRES_HOST', '127.0.0.1')
    port: int = os.environ.get('POSTGRES_PORT', 5430)
    # options: str = os.environ.get('DB_OPTIONS')


class Settings(BaseSettings):
    last_state_key: str = os.environ.get('ETL_STATE_KEY', None)
    state_file_path: str = os.environ.get('ETL_STATE_STORAGE', 'last_state.json')
    dsn: PostgresSettings = PostgresSettings()
    batch_size: int = os.environ.get('CHUNK_SIZE',100)
    es_host: str = os.environ.get('ES_URL', '127.0.0.1')
    offset_counter: int = 100


settings = Settings()
settings.dsn.user = 'app'
