"""Module with settings."""
import os
from pydantic import BaseSettings, Field
from dotenv import load_dotenv

load_dotenv()



class PostgresSettings(BaseSettings):
    dbname: str = os.environ.get('POSTGRES_DB')
    user: str = os.environ.get('POSTGRES_USER')
    password: str = os.environ.get('POSTGRES_PASSWORD')
    host: str = os.environ.get('POSTGRES_HOST')
    port: int = os.environ.get('POSTGRES_PORT')
    options: str = os.environ.get('DB_OPTIONS')


class Settings(BaseSettings):
    last_state_key_movies: str = os.environ.get('ETL_STATE_KEY_MOVIES')
    last_state_key_genres: str = os.environ.get('ETL_STATE_KEY_GENRES')
    last_state_key_persons: str = os.environ.get('ETL_STATE_KEY_PERSONS')
    state_file_path_movies: str = os.environ.get('ETL_STATE_STORAGE_MOVIES')
    state_file_path_genres: str = os.environ.get('ETL_STATE_STORAGE_GENRES')
    state_file_path_persons: str = os.environ.get('ETL_STATE_STORAGE_PERSONS')
    dsn: PostgresSettings = PostgresSettings()
    batch_size: int = os.environ.get('CHUNK_SIZE')
    es_host: str = os.environ.get('ES_URL')
    offset_counter_filmwork: int = 0
    offset_counter_genre: int = 0
    offset_counter_person: int = 0


settings = Settings()
