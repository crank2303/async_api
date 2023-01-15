"""Module for extract data from postgres."""
import logging

import backoff
import contextlib
import psycopg2
from psycopg2.extras import DictCursor

from settings import settings


class PostgresExtractor:
    """This class extracts data from psql."""

    @backoff.on_exception(backoff.expo, exception=ConnectionError)
    def extract_modified_data(self, date: str, query: dict, offset_counter: int):
        """Extract movies, checked modified movies.

        Returns:
            movies_modified_list(list): list with movies
        """
        print(settings.dsn.dict())
        with contextlib.closing(psycopg2.connect(**settings.dsn.dict(), cursor_factory=DictCursor)) \
                as conn, conn.cursor() as cursor:
            query = query.replace('modified','updated_at')%(date)
            cursor.execute(query)
            movies_modified_batch = cursor.fetchmany(settings.batch_size)
            if len(movies_modified_batch) == 0:
                return None
        logging.info("Data extracted from postgres!")
        return movies_modified_batch


if __name__ == '__main__':
    from queries import filmwork_query, genre_query, person_query
    import datetime
    from models.filmwork_model import Filmwork
    from models.genre_model import Genre
    from models.person_model import Person

    # задаем константу для обработки каждой схемы
    # ключ это наименование индекса
    # где query - запрос для каждой схемы
    # model это pydantic модель
    # fields это поля которые вернет нам запрос
    # pydantic будет игнорировать поля которые
    # не указаны в классе
    QUERIES = {
        'movies': {'query': filmwork_query.QUERY,
                     'model': Filmwork,
                     'fields': ['id', 'title', 'description',
                                'imdb_rating', 'type', 'creation_date',
                                'modified', 'director', 'actors', 'writers',
                                'genre'
                                ]},
        'genres': {'query': genre_query.QUERY,
                  'model': Genre,
                  'fields': ['id', 'name', 'description', 'modified']},
        'persons': {'query': person_query.QUERY,
                   'model': Person,
                   'fields': ['id', 'full_name', 'role', 'film_ids']},
    }

    date_time = datetime.datetime.min
    offset_counter = settings.offset_counter
    for schema in QUERIES:
        # получаем данные в зависимости от схемы с которой работаем
        all_movies = PostgresExtractor().extract_modified_data(
            date=date_time, query=QUERIES[schema]['query'],  offset_counter=offset_counter)

        # преобразуем список полученных данных в список словарей где ключи это fields
        query_list_of_dict = list(map(
            lambda x: dict(zip(QUERIES[schema]['fields'], x)), all_movies))

        # каждую запись преобразуем к соответствующей model pydantic
        models_list = [QUERIES[schema]['model'](**row) for row in query_list_of_dict]

        # готовим к записи в es
        es_list_of_dict = []
        for row in models_list:
            index_temp = {'index': {'_index': schema, '_id': str(row.id)}}
            data = row.__dict__
            es_list_of_dict.append(index_temp)
            es_list_of_dict.append(data)

        print(es_list_of_dict)
        # по идее эти данные можно пушить в es
        # es_conn.bulk(index=schema, body=es_list_of_dict)
