"""Схемы представления данных в api"""

from pydantic import BaseModel


class FilmAPI(BaseModel):
    id: str
    title: str
    imdb_rating: str


class PersonAPI(BaseModel):
    id: str
    full_name: str
    role: str
    film_ids: list[str]


class FilmData(BaseModel):
    role: str
    films_list: list[FilmAPI]