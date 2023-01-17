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
            'role': {
                'type': 'keyword'
            },
            'film_ids': {
                'type': 'keyword',
            }
        },
    },
}