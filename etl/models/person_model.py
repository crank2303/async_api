from uuid import UUID
from pydantic import BaseModel, validator
from pydantic.schema import Optional


class Person(BaseModel):
    id: UUID
    full_name: str
    role: Optional[str]
    film_ids: Optional[list]

    @validator('role')
    def valid_role(cls, v):
        if v is None:
            return ''
        return v

    @validator('film_ids')
    def valid_film_ids(cls, v):
        if v is None:
            return []
        return v


