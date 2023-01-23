from functools import lru_cache
from typing import Optional

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.person import Person
from services.mixins import CacheValue, ServiceMixin
from core.config import settings


class PersonService(ServiceMixin):
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic
        self._index_name = 'persons'

    async def get_by_id(self, person_id: str) -> Optional[Person]:

        cache_key = self._build_cache_key(
            [CacheValue(name='person_id', value=person_id)]
        )
        person = await self._person_from_cache(cache_key)
        if not person:
            person = await self._get_person_from_elastic(person_id)
            if not person:
                return None
            await self._put_person_to_cache(cache_key, person)
        return person

    async def get_list(self, params) -> list[Person]:
        doc = await self.elastic.search(
            index=self._index_name,
            from_=(params.number - 1) * params.size, size=params.size
        )
        return [Person(**d['_source']) for d in doc['hits']['hits']]

    
    async def get_search_list(self, params) -> Optional[list[Person]]: 
        if params.search_by_full_name is None:
            doc = await self.elastic.search(
                index=self._index_name,
                from_=(params.number - 1) * params.size, size=params.size
            )
            return [Person(**d['_source']) for d in doc['hits']['hits']]
        q = {
            'query': {
                'multi_match': {
                    'query': params.search_by_full_name,
                    'fuzziness': 'auto',
                    'fields': [
                        'full_name'
                    ]
                }
            }
        }
        doc = await self.elastic.search(
                                    index=self._index_name,
                                    from_=(params.number - 1) * params.size, 
                                    size=params.size,
                                    body=q
                                    )
        return [Person(**d['_source']) for d in doc['hits']['hits']]


    async def _get_person_from_elastic(self, person_id: str) -> Optional[Person]:
        try:
            doc = await self.elastic.get(self._index_name, person_id)
        except NotFoundError:
            return None
        return Person(**doc['_source'])

    async def _person_from_cache(self, person_id: str) -> Optional[Person]:
        data = await self.redis.get(person_id)
        if not data:
            return None
        person = Person.parse_raw(data)
        return person

    async def _put_person_to_cache(self, cache_key: str, person: Person):
        await self.redis.set(
            cache_key, person.json(), expire=settings.redis_cache_expire_seconds
        )


@lru_cache()
def get_person_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    return PersonService(redis, elastic)
