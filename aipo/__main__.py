import sys
import asyncio
import logging
from tkinter import Tk
from .app import App

# setup root logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s \t %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# ignore asyncio logs
logging.getLogger('asyncio').setLevel(logging.ERROR)


async def main() -> None:
    root = Tk()
    app = App(root)
    root.mainloop()
    await app.cleanup()


if __name__ == "__main__":
    asyncio.run(main())