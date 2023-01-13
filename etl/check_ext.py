from elasticsearch import Elasticsearch
from extractor import PostgresExtractor
from queries import query_movies
from transformer import DataTransformer

date_time = "2011-05-16 15:36:38"  # Выбираем дату с которой будет выполняться перенос фильмов
#
all_movies = PostgresExtractor().extract_modified_data(date=date_time, query=query_movies)  # Выполнение выгрузки данных из postgres
transformed_data = DataTransformer().data_to_es(data=all_movies, name_of_query=query_movies['name_of_query'])

#
# es = Elasticsearch(Settings().dict()['es_host'], request_timeout=300)
# es.indices.create(index=Settings().dict()['es_index_name'], body=Settings().dict()['index_json'])
#
print(transformed_data)

