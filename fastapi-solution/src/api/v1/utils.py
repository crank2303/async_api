from typing import Optional

from fastapi import Query


class GenreParams:
    def __init__(
        self,
        sort: Optional[str] = Query(
            "name",
            alias="sort",
            title="Сортировка по наименованию жанра",
            description=(
                "Сортирует по возрастанию и убыванию,"
                " -field если нужна сортировка"
                " по убыванию или field,"
                " если нужна сортировка по возрастанию."
                " По умолчанию сортирует по"
                " полю name в алфавитном порядке."
            ),
        ),
        number: Optional[int] = Query(
            1,
            alias="page[number]",
            title="страница",
            description="Порядковый номер страницы результатов",
        ),
        size: Optional[int] = Query(
            50,
            alias="page[size]",
            title="размер страницы",
            description="Количество документов на странице",
        ),
    ) -> None:
        self.sort = sort
        self.number = number
        self.size = size


class FilmParams:
    def __init__(
        self,
        sort: Optional[str] = Query(
            "imdb_rating",
            alias="sort",
            title="Сортировка по рейтингу",
            description=(
                "Сортирует по возрастанию и убыванию,"
                " -field если нужна сортировка"
                " по убыванию или field,"
                " если нужна сортировка по возрастанию."
                " По умолчанию сортирует по"
                " полю imdb_rating по возрастанию."
            ),
        ),
        number: Optional[int] = Query(
            1,
            alias="page[number]",
            title="страница",
            description="Порядковый номер страницы результатов",
        ),
        size: Optional[int] = Query(
            50,
            alias="page[size]",
            title="размер страницы",
            description="Количество документов на странице",
        ),
        filter: Optional[str] = Query(
            default=None,
            alias="filter",
            title="Фильтрация по жанрам",
            description=(
                "Фильтрует фильмы, оставляя только те,"
                "которые относятся к конкретному жанру."
            ),
        )
    ) -> None:
        self.sort = sort
        self.number = number
        self.size = size
        self.filter = filter
