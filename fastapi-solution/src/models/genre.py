from mixins import MixinConfig, MixinUUID


class Genre(MixinUUID, MixinConfig):
    name: str
    popular: float = 0.0
