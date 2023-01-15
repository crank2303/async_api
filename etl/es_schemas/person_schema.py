from es_schemas.settings import SETTINGS_DATA

PERSONS_INDEX_BODY: dict = {
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
            'actor_films': {
                'type': 'nested',
                'dynamic': 'strict',
                'properties': {
                    'id': {
                        'type': 'keyword',
                    },
                    'title': {
                        'type': 'text',
                        'analyzer': 'ru_en',
                    },
                },
            },
            'writer_films': {
                'type': 'nested',
                'dynamic': 'strict',
                'properties': {
                    'id': {
                        'type': 'keyword',
                    },
                    'title': {
                        'type': 'text',
                        'analyzer': 'ru_en',
                    },
                },
            },
            'director_films': {
                'type': 'nested',
                'dynamic': 'strict',
                'properties': {
                    'id': {
                        'type': 'keyword',
                    },
                    'title': {
                        'type': 'text',
                        'analyzer': 'ru_en',
                    },
                },
            },
        },
    },
}