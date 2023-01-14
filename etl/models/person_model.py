from uuid import UUID
from pydantic import BaseModel


class Person(BaseModel):
    id: UUID
    full_name: str
    role: str
    film_ids: list(UUID)


