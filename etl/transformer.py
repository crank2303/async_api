"""Module for transform data from postgres to ES."""
import logging

import backoff

from pydantic import BaseModel


class DataTransformer:
    """This class transform extracted data to format for request in ES."""

    @backoff.on_predicate(backoff.fibo, max_value=13)
    def data_to_es(
        self, 
        data: list, 
        model: BaseModel,
        fields: list[str],
        schema: str) -> str:
        """Extract movies, checked modified genres.

        Returns:
            tr_str(string): data formatted to request in ES
        """
        query_list_of_dict = list(map(lambda x: dict(zip(fields, x)), data))

        data_list = [model(**row) for row in query_list_of_dict]
        
        out = []
        for elem in data_list:
            index_template = {'index': {'_index': schema, '_id': str(elem.id) }}
            out.append(index_template)
            out.append(elem.dict())

        logging.info("Data transformed successfully.")
        return out
