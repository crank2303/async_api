"""Module for transform data from postgres to ES."""
import logging
from typing import Optional

import backoff

from models.filmwork_model import Filmwork
from models.genre_model import Genre
from models.person_model import Person
from queries.filmwork_query import QUERY_FILMWORK
from queries.genre_query import QUERY_GENRE
from queries.person_query import QUERY_PERSON


class DataTransformer:
    """This class transform extracted data to format for request in ES."""

    def data_to_es(self, data: Optional[list], name_of_query: str) -> Optional[str]:
        """Extract movies, checked modified genres.

        Returns:
            tr_str(string): data formatted to request in ES
        """
        if data is None:
            return None
        else:
            data_list = []
            for elem in data:
                query_config = {
                    'movies': Filmwork,
                    'persons': Person,
                    'genres': Genre
                }
                model = query_config.get(name_of_query)
                data_elem = model(**elem)
                data_list.append(data_elem)
            out = []
            for elem in data_list:
                index_template = "{\"index\": {\"_index\": " + f"\"{name_of_query}\", \"_id\": \"" + f"{str(elem.id)}" + "\"}}"
                out.append(index_template)
                out.append(elem.json())
            tr_str = "\n"
            for i in range(len(out)):
                tr_str = tr_str + str(out[i]) + "\n"
            logging.info("Data transformed successfully.")
            return tr_str
