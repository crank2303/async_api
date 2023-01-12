from mixins import MixinUUID, MixinConfig
from genre import Genre
from person import Person


class Film(MixinUUID, MixinConfig):
    imdb_rating: float = 0.0
    genre: list[Genre]
    title: str = ''
    description: str = ''
    director: list[Person]
    actor_names: list[Person]
    writers_name: list[Person]


