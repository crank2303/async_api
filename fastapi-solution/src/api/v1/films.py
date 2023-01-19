from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException

from api.v1.utils import FilmParams
from models.film import Film
from services.film import FilmService, get_film_service

NO_FILMS = "Не удалось получить фильмы из Elasticsearch."
FILM_NOT_FOUND = "Фильм с uuid {uuid} не найден в Elasticsearch."

router = APIRouter()


@router.get(
    path="/",
    response_model=list[Film],
    summary="Главная страница фильмов",
    description="Полный перечень фильмов",
    response_description="Список с неполной информацией о фильмах",
)
async def get_films(
    params: FilmParams = Depends(),
    film_service: FilmService = Depends(get_film_service),
) -> list[Film]:
    es_films = await film_service.get_list(params)
    if not es_films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=NO_FILMS)
    films = [Film(id=film.id,
                  title=film.title,
                  imdb_rating=film.imdb_rating) for film in es_films]
    return films


@router.get(
    "/{uuid}",
    response_model=Optional[Film],
    summary="Поиск фильма по UUID",
    description="Поиск фильма по UUID",
    response_description="Полная информация о фильме",
)
async def film_details(
    uuid: str, film_service: FilmService = Depends(get_film_service)
) -> Optional[Film]:
    es_film = await film_service.get_by_id(uuid)
    if not es_film:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=FILM_NOT_FOUND.format(uuid=uuid),
        )
    return Film(id=es_film.id,
                title=es_film.title,
                imdb_rating=es_film.imdb_rating,
                description=es_film.description,
                genre=es_film.genre,
                actors=es_film.actors,
                writers=es_film.writers,
                director=es_film.director)
