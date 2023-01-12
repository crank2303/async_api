from mixins import MixinUUID, MixinConfig

class Person(MixinUUID, MixinConfig):
    full_name: str