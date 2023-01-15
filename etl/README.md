## TODO

- es_schema - удалить
- models - перенести в папку models, модель movies
- README - везде потом удалить

Пример для **loader.py**

```python
from queries.person_query import QUERY_PERSON
from queries.genre_query import QUERY_GENRE
from queries.filmwork_query import QUERY_FILMWORK

QUERIES = {
    "persons": PERSON_QUERY,
    "genres": GENRE_QUERY,
    "movies": QUERY_FILMWORK,
}

def create_index(self):
    """Create index in ES."""
    for index in QUERIES:
        if not self.es.indices.exists(index=index):
            self.es.indices.create(index=index, body=index_json)
            logging.info("Index in ES created!")
```
