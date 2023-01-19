from functools import lru_cache
from typing import Optional

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from core import config
from db.elastic import get_elastic
from db.redis import get_redis
from models.film import Film
from services.mixins import CacheValue, ServiceMixin


class FilmService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic
        self._index_name = 'movies'

    async def get_by_id(self, film_id: str) -> Optional[Film]:
        cache_key = self._build_cache_key(
            [CacheValue(name='film_id', value=film_id)]
        )
        film = await self._film_from_cache(cache_key)
        if not film:
            film = await self._get_film_from_elastic(film_id)
            if not film:
                return None
            await self._put_film_to_cache(cache_key, film)
        return film

    async def get_list(self, params):
        if params.filter is None:
            doc = await self.elastic.search(
                index=self._index_name,
                from_=(params.number - 1) * params.size, size=params.size
            )
            return [Film(**d["_source"]) for d in doc["hits"]["hits"]]
        else:
            doc = await self.elastic.search(
                index=self._index_name,
                from_=(params.number - 1) * params.size, size=params.size,
                body={
                    "query": {
                        "bool": {
                            "must": [
                                {
                                    "match": {
                                        "genre": {
                                            "id": params.filter
                                        }
                                    }
                                }
                            ]
                        }
                    }
                }
            )
        return [Film(**d["_source"]) for d in doc["hits"]["hits"]]

    async def _get_film_from_elastic(self, film_id: str) -> Optional[Film]:
        try:
            doc = await self.elastic.get('movies', film_id)
        except NotFoundError:
            return None
        return Film(**doc['_source'])

    async def _film_from_cache(self, film_id: str) -> Optional[Film]:
        data = await self.redis.get(film_id)
        if not data:
            return None
        film = Film.parse_raw(data)
        return film

    async def _put_film_to_cache(self, cache_key: str, film: Film):
        await self.redis.set(
            cache_key, film.json(), expire=config.REDIS_CACHE_EXPIRE_SECONDS
        )


@lru_cache()
def get_film_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic)
