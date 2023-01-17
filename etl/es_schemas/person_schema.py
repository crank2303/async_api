from es_schemas.settings import SETTINGS_DATA

SCHEMA: dict = {
    **SETTINGS_DATA,
    'mappings': {
        'dynamic': 'strict',
        'properties': {
            'id': {
                'type': 'keyword',
            },
            'full_name': {
                'type': 'text',
                'analyzer': 'ru_en',
                'fields': {
                    'raw': {
                        'type': 'keyword',
                    },
                },
            },
            'film_ids_actor': {
                'type': 'keyword',
            },
            'film_ids_writer': {
                'type': 'keyword',
            },
            'film_ids_director': {
                'type': 'keyword',
            },
        },
    },
}