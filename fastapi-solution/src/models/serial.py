from mixins import MixinUUID, MixinConfig
from genre import Genre
from person import Person


class Serial(MixinUUID, MixinConfig):
    title: str
    imdb_rating: float = 0.0
    description: str
    genre: list[Genre]
    actors: list[Person]
    writers: list[Person]
    directors: list[Person]
