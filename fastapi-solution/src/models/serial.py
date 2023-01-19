from mixins import MixinUUID, MixinConfig
from genre import Genre
from person import Person


class Serial(MixinUUID, MixinConfig):
    id: str
    title: str = ''
    imdb_rating: float = 0.0
    description: str = ''
    genre: list[Genre]
    actors: list[Person]
    writers: list[Person]
    director: list[Person]
