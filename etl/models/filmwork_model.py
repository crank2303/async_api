from uuid import UUID

from pydantic import BaseModel, validator
from pydantic.schema import List, Optional


class Filmwork(BaseModel):

    id: UUID
    imdb_rating: Optional[float]
    mpaa_rating: Optional[str]
    genre: Optional[List]
    title: str
    description: Optional[str]
    director: Optional[List]
    actors: Optional[List]
    writers: Optional[List]

    @validator('description')
    def valid_description(cls, value):
        if value is None:
            return ''
        return value

    @validator('director')
    def valid_director(cls, value):
        if value is None:
            return []
        return value

    @validator('actors')
    def valid_actors(cls, value):
        if value is None:
            return []
        return value

    @validator('writers')
    def valid_writers(cls, value):
        if value is None:
            return []
        return value

    @validator('mpaa_rating')
    def valid_mpaa_rating(cls, value):
        if value is None:
            return ''
        return value
