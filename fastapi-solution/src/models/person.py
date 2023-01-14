from uuid import UUID
from mixins import MixinUUID, MixinConfig
from pydantic import Field


class Person(MixinUUID, MixinConfig):
    full_name: str
    role: str
    film_ids: list(UUID) = Field(exclude=True)