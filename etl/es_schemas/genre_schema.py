from es_schemas.settings import SETTINGS_DATA

GENRES_INDEX_BODY: dict = {
    **SETTINGS_DATA,
    "mappings": {
        "dynamic": "strict",
        "properties": {
            "id": {"type": "keyword"},
            "name": {"type": "keyword"},
            "description": {"type": "text", "analyzer": "ru_en"},
        },
    },
}
