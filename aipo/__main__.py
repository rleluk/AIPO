import sys
import logging
from tkinter import Tk
from .app import App

# setup root logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


if __name__ == "__main__":
    try:
        root = Tk()
        app = App(root)
        root.mainloop()
    finally: 
        app.cleanup()
    

