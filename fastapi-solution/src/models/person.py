from uuid import UUID
from models.mixins import MixinConfig


class Person(MixinConfig):
    id: str
    full_name: str
    film_ids_director: list[str]
    film_ids_writer: list[str] 
    film_ids_actor: list[str]