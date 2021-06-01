import logging
import aiohttp
from typing import Tuple

from .config import UbidotsConfig


logger = logging.getLogger(__name__)


class UbidotsClient:

    @classmethod
    def from_config(cls, config: UbidotsConfig):
        if config.url is None or config.token is None:
            logger.warning("No ubidots config - cannot create client's session") 
            return None
        
        self = cls.__new__(cls)
        self._config = config
        self._session = aiohttp.ClientSession()
        logger.debug("Creating aiohttp client's session")
        return self

    async def send_request(self, variable:str, value: int) -> Tuple[dict, int]:
        headers = {
            "X-Auth-Token": self._config.token, 
            "Content-Type": "application/json"
        }

        payload = {
            variable: {
                "value": value,
            }
        }

        logger.debug(f"Sending new data to Ubidots service: {payload}")
        async with self._session.post(self._config.url, headers=headers, json=payload) as response:
            json_response = await response.json()
            logger.debug(f"Response status: {response.status}, content: {json_response}")
            return json_response, response.status

    async def delete_session(self) -> None:
        logger.debug("Closing aiohttp client's session")
        await self._session.close()
