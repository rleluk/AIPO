from decouple import config
from typing import NamedTuple


class UbidotsConfig(NamedTuple):
    url: str
    token: str


def load_ubidots_config() -> UbidotsConfig:
    return UbidotsConfig(
        url=config('URL', None),
        token=config('TOKEN', None),
    )
