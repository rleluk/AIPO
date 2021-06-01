import asyncio
import logging
from threading import Thread


logger = logging.getLogger(__name__)


thread_loop = asyncio.get_event_loop()


def start_loop(loop):
    try:
        asyncio.set_event_loop(loop)
        loop.run_forever()
    except Exception as err:
        logger.err(err)


thread = Thread(target=start_loop, args=(thread_loop,), daemon=True)
thread.start()
