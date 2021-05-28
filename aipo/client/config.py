from decouple import config
from typing import NamedTuple


class UbidotsConfig(NamedTuple):
    url: str
    token: str
    variable: str


def load_ubidots_config() -> UbidotsConfig:
    return UbidotsConfig(
        url=config('URL'),
        token=config('TOKEN'),
        variable=config('VARIABLE')
    )