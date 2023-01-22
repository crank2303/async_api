from pydantic import BaseModel

from models.mixins import  MixinConfig
from models.genre import Genre


class Person(MixinConfig):
    id: str
    name: str

class Serial(MixinConfig):
    id: str
    title: str = ''
    imdb_rating: float = 0.0
    description: str = ''
    genre: list[Genre]
    actors: list[Person]
    writers: list[Person]
    director: list[Person]
