"""Module for load data to ES."""
import datetime
import logging

from elasticsearch import Elasticsearch

from es_schemas.genre_schema import SCHEMA as GENRES_INDEX_BODY
from es_schemas.filmwork_schema import SCHEMA as FILMWORKS_INDEX_BODY
from es_schemas.person_schema import SCHEMA as PERSONS_INDEX_BODY
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

    def bulk_create(self, data, state: State):
        """Create bulk in ES."""
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        state.set_state(settings.last_state_key, now)
        self.es.bulk(index=settings.es_index_name, body=data)
        logging.info("Data loaded in ES!")
