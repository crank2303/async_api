from uuid import UUID
from models.mixins import MixinConfig
from pydantic import Field


class Person(MixinConfig):
    id: str
    full_name: str
    film_ids_director: list[UUID]
    film_ids_writer: list[UUID] 
    film_ids_actor: list[UUID]