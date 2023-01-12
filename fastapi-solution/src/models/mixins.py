import orjson

from pydantic import BaseModel
from pydantic.schema import Optional 


def orjson_dumps(v, *, default):
    # orjson.dumps возвращает bytes, а pydantic требует unicode, поэтому декодируем
    return orjson.dumps(v, default=default).decode()


class MixinUUID(BaseModel):
    id: str


class MixinConfig():

    class Config:
        # Заменяем стандартную работу с json на более быструю
        json_loads = orjson.loads
        json_dumps = orjson_dumps
