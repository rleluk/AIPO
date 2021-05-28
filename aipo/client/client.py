import logging
import aiohttp
from typing import Any

from .config import UbidotsConfig


logger = logging.getLogger(__name__)


class UbidotsClient:

    def __init__(self, config: UbidotsConfig) -> None:
        self._config = config
        self._session = aiohttp.ClientSession()
        logger.debug("Creating aiohttp client's session")

    async def send_request(self, value: int, context: Any) -> None:
        headers = {
            "X-Auth-Token": self._config.token, 
            "Content-Type": "application/json"
        }

        payload = {
            self._config.variable: {
                "value": value,
                "context": context
            }
        }

        logger.debug(f"Sending new data to Ubidots service: {payload}")
        async with self._session.post(self._config.url, headers=headers, json=payload) as response:
            if response.status != 201:
                logger.error(await response.text())
            else:
                logger.debug(await response.json())

    async def delete_session(self) -> None:
        logger.debug("Closing aiohttp client's session")
        await self._session.close()
