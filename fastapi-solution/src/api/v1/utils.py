from typing import Optional

from fastapi import Query, Path


class GenreParams:
    def __init__(
        self,
        sort: Optional[str] = Query(
            'name',
            alias='sort',
            title='Сортировка по наименованию жанра',
            description=(
                'Сортирует по возрастанию и убыванию,'
                ' -field если нужна сортировка'
                ' по убыванию или field,'
                ' если нужна сортировка по возрастанию.'
                ' По умолчанию сортирует по'
                ' полю name в алфавитном порядке.'
            ),
        ),
        number: Optional[int] = Query(
            1,
            alias='page[number]',
            title='страница',
            description='Порядковый номер страницы результатов',
            ge=1,
        ),
        size: Optional[int] = Query(
            50,
            alias='page[size]',
            title='размер страницы',
            description='Количество документов на странице',
            ge=1,
        ),
    ) -> None:
        self.sort = sort
        self.number = number
        self.size = size


class FilmParams:
    def __init__(
        self,
        sort: Optional[str] = Query(
            'imdb_rating',
            alias='sort',
            title='Сортировка по рейтингу',
        description=(
                'Сортирует по возрастанию и убыванию,'
                ' -field если нужна сортировка'
                ' по убыванию или field,'
                ' если нужна сортировка по возрастанию.'
                ' По умолчанию сортирует по'
                ' полю imdb_rating по возрастанию.'
                ),
        ),
        number: Optional[int] = Query(
            default=1,
            alias='page[number]',
            title='страница',
            description='Порядковый номер страницы результатов',
            ge=1,
        ),
        size: Optional[int] = Query(
            50,
            alias='page[size]',
            title='размер страницы',
            description='Количество документов на странице',
            ge=1,
        ),
        filter: Optional[str] = Query(
        default=None,
        alias='filter',
        title='Фильтрация по жанрам',
        description=(
            'Фильтрует фильмы, оставляя только те,'
            'которые относятся к конкретному жанру.'
        ),
        )
    ) -> None:
        self.sort = sort
        self.number = number
        self.size = size
        self.filter = filter
        

class PersonParams:
    def __init__(
        self,
        sort: Optional[str] = Query(
            'full_name',
            alias='sort',
            title='Сортировка по имени',
            description=(
                'Сортирует по возрастанию и убыванию,'
                ' -field если нужна сортировка'
                ' по убыванию или field,'
                ' если нужна сортировка по возрастанию.'
                ' По умолчанию сортирует по'
                ' полю name в алфавитном порядке.'
               ),
        ),
        number: Optional[int] = Query(
            1,
            alias='page[number]',
            title='страница',
            description='Порядковый номер страницы результатов',
            ge=1,
        ),
        size: Optional[int] = Query(
            50,
            alias='page[size]',
            title='размер страницы',
            description='Количество документов на странице',
            ge=1,
        ),
          ) -> None:
        self.sort = sort
        self.number = number
        self.size = size
        

class FilmSearchParams:
    def __init__(
        self,
        search_by_title: Optional[str] = Query(
            '',
            alias='search_by_title',
            title='Поиск по наименованию',
        description=(
                'Ищет фильмы по наименованию,'
                ' предлагает ревелантные результаты'
                ),
        ),
        number: Optional[int] = Query(
            1,
            alias='page[number]',
            title='страница',
            description='Порядковый номер страницы результатов',
            ge=1,
        ),
        size: Optional[int] = Query(
            50,
            alias='page[size]',
            title='размер страницы',
            description='Количество документов на странице',
            ge=1,
        )
    ) -> None:
        self.search_by_title = search_by_title
        self.number = number
        self.size = size


class PersonSearchParams:
    def __init__(
        self,
        search_by_full_name: Optional[str] = Query(
            '',
            alias='search_by_title',
            title='Поиск по имени',
        description=(
                'Ищет фильмы по имени,'
                ' предлагает ревелантные результаты'
                ),
        ),
        number: Optional[int] = Query(
            1,
            alias='page[number]',
            title='страница',
            description='Порядковый номер страницы результатов',
            ge=1,
        ),
        size: Optional[int] = Query(
            50,
            alias='page[size]',
            title='размер страницы',
            description='Количество документов на странице',
            ge=1,
        )
    ) -> None:
        self.search_by_full_name = search_by_full_name
        self.number = number
        self.size = size
