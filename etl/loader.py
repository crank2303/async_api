"""Module for load data to ES."""
import datetime
import logging

from elasticsearch import Elasticsearch

from es_schemas.genre_schema import GENRES_INDEX_BODY
from es_schemas.filmwork_schema import FILMWORKS_INDEX_BODY
from es_schemas.person_schema import PERSONS_INDEX_BODY
from settings import settings
from state import State

INDEXES = {
    "persons": PERSONS_INDEX_BODY,
    "genres": GENRES_INDEX_BODY,
    "movies": FILMWORKS_INDEX_BODY,
}


class ElasticsearchLoader:
    """This class load data in ES."""

    def __init__(self, es: Elasticsearch):
        """Take ElasticSearch connection."""
        self.es = es

    def create_index(self):
        """Create index in ES."""
        for index in INDEXES:
            if not self.es.indices.exists(index=index):
                self.es.indices.create(index=index, body=INDEXES[index])
                logging.info("Index in ES created!")

    def bulk_create(self, data, state: State, name_of_data: str):
        """Create bulk in ES."""
        if data is None:
            return None
        else:
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if name_of_data == "movies":
                state.set_state(settings.last_state_key_movies, now)
            elif name_of_data == "genres":
                state.set_state(settings.last_state_key_genres, now)
            elif name_of_data == "persons":
                state.set_state(settings.last_state_key_persons, now)
            self.es.bulk(index=name_of_data, body=data)
            logging.info("Data loaded in ES!")
