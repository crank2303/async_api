"""Main ETL-module."""
import datetime
import logging
import time

from elasticsearch import Elasticsearch

from extractor import PostgresExtractor
from loader import ElasticsearchLoader
from queries import filmwork_query, genre_query, person_query
from settings import settings
from state import JsonFileStorage, State
from transformer import DataTransformer
from models.filmwork_model import Filmwork
from models.genre_model import Genre
from models.person_model import Person


INDEX = {
    'movies': {'query': filmwork_query.QUERY,
                'model': Filmwork,
                'fields': ['id', 'title', 'description',
                            'imdb_rating', 'type', 'creation_date',
                            'modified', 'director', 'actors', 'writers',
                            'genre'
                            ],
                'update_date': datetime.datetime.min,
                'offset_counter': settings.offset_counter},

    'genres': {'query': genre_query.QUERY,
                'model': Genre,
                'fields': ['id', 'name', 'description', 'modified'],
                'update_date': datetime.datetime.min,
                'offset_counter': settings.offset_counter},

    'persons': {'query': person_query.QUERY,
                'model': Person,
                'fields': ['id', 'full_name', 'role', 'film_ids'],
                'update_date': datetime.datetime.min,
                'offset_counter': settings.offset_counter},
}


def main():
    
    es = Elasticsearch(settings.es_host, request_timeout=300)
    ElasticsearchLoader(es).create_index()  # Создание индекса
    
    storage = JsonFileStorage(settings.state_file_path)  # Создание хранилища на основе файла
    state = State(storage)  # Создание состояния, привязанного к хранилищу

    while True:

        for schema in INDEX:
            all_data = PostgresExtractor().extract_modified_data(
                date=INDEX[schema]['update_date'], query=INDEX[schema]['query'],
                 offset_counter=INDEX[schema]['offset_counter'])                 

            if all_data is None:
                logging.info("No data")
                INDEX[schema]['update_date'] = state.get_state(schema + '_last_update')
                INDEX[schema]['offset_counter'] = 0
                time.sleep(30)
                continue

            transformed_data = DataTransformer().data_to_es(
                data=all_data, schema=schema, 
                model=INDEX[schema]['model'], fields=INDEX[schema]['fields'],
                )

            ElasticsearchLoader(es).bulk_create(
                data=transformed_data, state=state, schema=schema)
            logging.info("Batch is loaded")
            time.sleep(5)
            
            INDEX[schema]['offset_counter'] += 1


if __name__ == '__main__':
    main()
