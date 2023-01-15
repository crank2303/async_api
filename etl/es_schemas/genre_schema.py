from settings import SETTINGS_DATA

SCHEMA: dict = {
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
