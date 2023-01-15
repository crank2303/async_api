from uuid import UUID
from pydantic import BaseModel, validator
from pydantic.schema import Optional, List


class Person(BaseModel):
    id: UUID
    full_name: str
    actor_films: Optional[List]
    writer_films: Optional[List]
    director_films: Optional[List]

    @validator('actor_films')
    def valid_actor_films(cls, value):
        if value is None:
            return []
        return value

    @validator('writer_films')
    def valid_writer_films(cls, value):
        if value is None:
            return []
        return value

    @validator('director_films')
    def valid_director_films(cls, value):
        if value is None:
            return []
        return value

    @validator('full_name')
    def valid_full_name(cls, value):
        if value is None:
            return ''
        return value
