from http import HTTPStatus
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from api.v1.utils import PersonParams, PersonSearchParams
from api.v1.schemas import PersonAPI, FilmAPI, FilmData
from api.v1.contstants import NO_PERSON, PERSON_NOT_FOUND
from models.person import Person
from services.persons import PersonService, get_person_service
from services.film import FilmService, get_film_service


router = APIRouter()


@router.get(
    path='/',
    response_model=list[PersonAPI],
    summary='Полный перечень людей',
    description='Полный перечень людей',
    response_description='Список с полной информацией фильмов в которых принимали участие',
)
async def get_persons(
    params: PersonParams = Depends(),
    person_service: PersonService = Depends(get_person_service),
) -> list[PersonAPI]:

    es_persons = await person_service.get_list(params)
    if not es_persons:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=NO_PERSON)
    
    persons = await prepare_person(es_persons)
    if params.sort:
        rev = False if '-' in params.sort else True
        params.sort = params.sort.replace('-', '')
        persons = sorted(persons, key=lambda x: x.dict()[params.sort], reverse=rev)
    return persons


@router.get(
    path='/search',
    response_model=list[PersonAPI],
    summary='Поиск по имени',
    description='Поиск по имени',
    response_description='Список ревелантных результатов',
)
async def get_search_persons(
    params: PersonSearchParams = Depends(),
    person_service: PersonService = Depends(get_person_service),
) -> list[PersonAPI]:

    es_persons = await person_service.get_search_list(params)
    if not es_persons:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=NO_PERSON)
    
    persons = await prepare_person(es_persons)
    return persons


async def prepare_person(persons: list[Person]) -> list [PersonAPI]:
    '''Преобразует к виду класса PersonAPI
    
    Args:
        persons: список людей
        
    Returns:
        list[PersonAPI]: преобразованные данные для вывода в api
    '''

    person_fast_api = []
    for person in persons:
        if person.film_ids_director:
           
           person_fast_api.append(PersonAPI(id=person.id,
                    full_name=person.full_name,
                    role='director',
                    film_ids=person.film_ids_director))

        if person.film_ids_actor:
            person_fast_api.append(PersonAPI(id=person.id,
                    full_name=person.full_name,
                    role='actor',
                    film_ids=person.film_ids_actor))

        if person.film_ids_writer:
            person_fast_api.append(PersonAPI(id=person.id,
                    full_name=person.full_name,
                    role='writer',
                    film_ids=person.film_ids_writer))
    
    return person_fast_api


@router.get(
    '/{uuid}',
    response_model=Optional[list[PersonAPI]],
    summary='Поиск актера по UUID',
    description='Поиск актера по UUID',
    response_description='Полная информация о человеке',
)
async def person_details(
    uuid: str, 
    person_service: PersonService=Depends(get_person_service)
) -> Optional[list[PersonAPI]]:
    es_person = await person_service.get_by_id(uuid)
    if not es_person:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=PERSON_NOT_FOUND.format(uuid=uuid),
        )

    person = await prepare_person([es_person])
    return person


@router.get(
    '/{uuid}/film',
    response_model=list[FilmData],
    summary='Информация о фильмах',
    description='Информация о всех фильмах в которых человек принимал участие',
    response_description='Полная информация о фильмах',
)
async def person_films(
    uuid: str, 
    person_service: PersonService=Depends(get_person_service),
    film_service: FilmService=Depends(get_film_service),
    ) -> list[FilmData]:
    '''Формирует подробную информаю о фильмах которые/которых снимался человек
    
    Args:
        uuid: id человека
        person_service: экземляр класса PersonService
        film_service: экземляр класса FilmService

    Return:
        list[FilmData]: список информации о фильмах по опрделенной роли
    '''

    person_roles_films: list[PersonAPI] = await person_details(
        uuid, person_service) 
    role_films = []
    for person_role_films in person_roles_films:
        films_info = await get_film_info(person_role_films.film_ids, film_service)
        role_films.append(FilmData(role=person_role_films.role,
                                films_list=films_info))
    return role_films


async def get_film_info(
    films_ids: list[UUID],
    film_service: FilmService=Depends(get_film_service),
    )->list[FilmAPI]:
    '''Получает данные по одной роли о фильмах из es
    
    Args:
        films_ids: id фильмов
        film_service: экземпляр класса FilmService

    Return:
        list[FilmAPI]: список информации о фильмах
    '''

    films_data = []
    for film_id in films_ids:
        es_film = await film_service.get_by_id(film_id)
        films_data.append(FilmAPI(uuid=es_film.id,
                                title=es_film.title,
                                imdb_rating=es_film.imdb_rating
                                ))
    return films_data
