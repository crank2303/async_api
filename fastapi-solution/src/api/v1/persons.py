from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException

from api.v1.utils import PersonParams
from models.person import Person
from services.persons import PersonService, get_person_service

NO_PERSON = "Не удалось получить данные о людях из Elasticsearch."
PERSON_NOT_FOUND = "Человек с uuid {uuid} не найден в Elasticsearch."

router = APIRouter()


@router.get(
    path="/",
    response_model=list[Person],
    summary="Главная страница",
    description="Полный перечень людей",
    response_description="Список с полной информацией фильмов в которых принимали участие",
)
async def get_persons(
    params: PersonParams = Depends(),
    person_service: PersonParams = Depends(get_person_service),
) -> list[Person]:
    es_persons = await person_service.get_list(params)
    if not es_persons:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=NO_PERSON)
    persons = [Person(id=person.id,
                    full_name=person.full_name,
                    film_ids_director=person.film_ids_director,
                    film_ids_writer=person.film_ids_writer,
                    film_ids_actor=person.film_ids_actor) for person in es_persons]
    return persons


@router.get(
    "/{uuid}",
    response_model=Optional[Person],
    summary="Поиск актера по UUID",
    description="Поиск актера по UUID",
    response_description="Полная информация о человеке",
)
async def person_details(
    uuid: str, person_service: PersonService = Depends(get_person_service)
) -> Optional[Person]:
    es_person = await person_service.get_by_id(uuid)
    if not es_person:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=PERSON_NOT_FOUND.format(uuid=uuid),
        )
    return Person(id=es_person.id,
                full_name=es_person.full_name,
                film_ids_director=es_person.film_ids_director,
                film_ids_writer=es_person.film_ids_writer,
                film_ids_actor=es_person.film_ids_actor)
