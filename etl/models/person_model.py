from uuid import UUID
from pydantic import BaseModel, validator
from pydantic.schema import Optional


class Person(BaseModel):
    id: UUID
    full_name: str
    film_ids_director: Optional[list[UUID]]
    film_ids_writer: Optional[list[UUID]]
    film_ids_actor: Optional[list[UUID]]

    @validator('film_ids_director')
    def valid_film_ids_director(cls, v):
        if v is None:
            return []
        return v

    @validator('film_ids_writer')
    def valid_film_ids_writer(cls, v):
        if v is None:
            return []
        return v

    @validator('film_ids_actor')
    def valid_film_ids_actor(cls, v):
        if v is None:
            return []
        return v


