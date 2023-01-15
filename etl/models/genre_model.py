from uuid import UUID
from pydantic import BaseModel
from pydantic.schema import Optional


class Genre(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None
