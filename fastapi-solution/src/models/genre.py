from models.mixins import MixinConfig


class Genre(MixinConfig):
    id: str
    name: str
    popular: float = 0.0
    description: str = None
