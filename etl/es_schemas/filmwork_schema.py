from es_schemas.settings import SETTINGS_DATA

SCHEMA: dict = {
    **SETTINGS_DATA,
    'mappings': {
        'dynamic': 'strict',
        'properties': {
            'id': {
                'type': 'keyword',
            },
            'imdb_rating': {
                'type': 'float',
            },
            'mpaa_rating': {
                'type': 'text',
            },
            'genre': {
                'type': 'nested',
                'dynamic': 'strict',
                'properties': {
                    'name': {
                        'type': 'text',
                        'analyzer': 'ru_en',
                    },
                    'id': {
                        'type': 'keyword',
                    },
                }
            },
            'title': {
                'type': 'text',
                'analyzer': 'ru_en',
                'fields': {
                    'raw': {
                        'type': 'keyword',
                    },
                },
            },
            'description': {
                'type': 'text',
                'analyzer': 'ru_en',
            },
            'director': {
                'type': 'nested',
                'dynamic': 'strict',
                'properties': {
                    'id': {
                        'type': 'keyword',
                    },
                    'name': {
                        'type': 'text',
                        'analyzer': 'ru_en',
                    },
                },
            },
            'actors': {
                'type': 'nested',
                'dynamic': 'strict',
                'properties': {
                    'id': {
                        'type': 'keyword',
                    },
                    'name': {
                        'type': 'text',
                        'analyzer': 'ru_en',
                    },
                },
            },
            'writers': {
                'type': 'nested',
                'dynamic': 'strict',
                'properties': {
                    'id': {
                        'type': 'keyword',
                    },
                    'name': {
                        'type': 'text',
                        'analyzer': 'ru_en',
                    },
                },
            },
        },
    },
}
