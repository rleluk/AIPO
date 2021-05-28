import typing
import logging
import tkinter as tk

from .client import UbidotsClient, load_ubidots_config


logger = logging.getLogger(__name__)


class App:
    
    def __init__(self, root: tk.Tk) -> None:
        self._window_root = root
        self._ubidots_client = UbidotsClient(load_ubidots_config())

    async def cleanup(self) -> None:
        await self._ubidots_client.delete_session()
