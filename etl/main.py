"""Main ETL-module."""
import datetime
import logging
import time

from elasticsearch import Elasticsearch

from extractor import PostgresExtractor
from loader import ElasticsearchLoader
from settings import settings
from state import JsonFileStorage, State
from transformer import DataTransformer
from queries.person_query import QUERY_PERSON
from queries.genre_query import QUERY_GENRE
from queries.filmwork_query import QUERY_FILMWORK


def main():
    date_time_movies = datetime.datetime.min  # Выбираем дату с которой будет выполняться перенос фильмов
    date_time_genres = datetime.datetime.min
    date_time_persons = datetime.datetime.min
    es = Elasticsearch(settings.es_host, request_timeout=300)
    ElasticsearchLoader(es).create_index()  # Создание индекса
    storage_movies = JsonFileStorage(settings.state_file_path_movies)  # Создание хранилища на основе файла
    storage_genres = JsonFileStorage(settings.state_file_path_genres)
    storage_persons = JsonFileStorage(settings.state_file_path_persons)
    state_movies = State(storage_movies)  # Создание состояния, привязанного к хранилищу
    state_genres = State(storage_genres)
    state_persons = State(storage_persons)
    offset_counter_filmwork = settings.offset_counter_filmwork
    offset_counter_genre = settings.offset_counter_genre
    offset_counter_person = settings.offset_counter_person
    while True:
        movies_from_postgres = PostgresExtractor().extract_modified_data(date=date_time_movies, query=QUERY_FILMWORK,
                                                               offset_counter=offset_counter_filmwork)
        offset_counter_filmwork += 1
        if movies_from_postgres is None:
            logging.info("No data")
            date_time_movies = state_movies.get_state('last_update_movies')
            offset_counter_filmwork = 0
        else:
            transformed_movies_from_postgres = DataTransformer().data_to_es(data=movies_from_postgres,
                                                                            name_of_query='movies')
            ElasticsearchLoader(es).bulk_create(data=transformed_movies_from_postgres, state=state_movies, name_of_data='movies')

        logging.info("Batch of movie is loaded")
        time.sleep(1)

        genres_from_postgres = PostgresExtractor().extract_modified_data(date=date_time_genres, query=QUERY_GENRE,
                                                                         offset_counter=offset_counter_genre)
        offset_counter_genre += 1
        if genres_from_postgres is None:
            logging.info("No data")
            date_time_genres = state_genres.get_state('last_update_genres')
            offset_counter_genre = 0
        else:
            transformed_genres_from_postgres = DataTransformer().data_to_es(data=genres_from_postgres, name_of_query='genres')
            ElasticsearchLoader(es).bulk_create(data=transformed_genres_from_postgres, state=state_genres, name_of_data='genres')
            logging.info("Batch of genre is loaded")
        time.sleep(1)

        persons_from_postgres = PostgresExtractor().extract_modified_data(date=date_time_persons, query=QUERY_PERSON,
                                                                         offset_counter=offset_counter_person)
        offset_counter_person += 1
        if persons_from_postgres is None:
            logging.info("No data")
            date_time_persons = state_persons.get_state('last_update_persons')
            offset_counter_person = 0
            print("person all")
        else:
            transformed_persons_from_postgres = DataTransformer().data_to_es(data=persons_from_postgres,
                                                                            name_of_query='persons')
            ElasticsearchLoader(es).bulk_create(data=transformed_persons_from_postgres, state=state_persons, name_of_data='persons')
            logging.info("Batch of person is loaded")
        time.sleep(1)

if __name__ == '__main__':
    main()
