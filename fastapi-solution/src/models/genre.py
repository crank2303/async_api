from models.mixins import MixinConfig


class Genre(MixinConfig):
    name: str
    popular: float = 0.0
    description: str = None
