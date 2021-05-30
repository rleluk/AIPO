import time
import logging
import threading
import tkinter as tk
from typing import Optional
from PIL import Image, ImageTk
from tkinter import Toplevel, filedialog as fd

from .client import UbidotsClient, load_ubidots_config
from .detector import PeopleDetector


logger = logging.getLogger(__name__)


class App:
    
    def __init__(self, root: tk.Tk):
        self._root = root
        self._people_detector = PeopleDetector()
        self._ubidots_client = UbidotsClient.from_config(load_ubidots_config())
        self._add_widgets()

    def _add_widgets(self) -> None:
        self._root.minsize(200, 300)
        self._root.resizable(False, False)
        self._root.title("People detector")

        tk.Button(text='Process image', command=self._detect_in_image)\
            .grid(column=0, row=0, pady=10)
        tk.Button(text='Process video', command=self._detect_in_sequence)\
            .grid(column=0, row=1, pady=10)

    def _detect_in_image(self) -> None:
        path = fd.askopenfilename()
        if not path:
            logger.error("Image path is empty")
            return
            
        image, count = self._people_detector.detect_in_image(path)
        if image is not None:
            _, label = self._spawn_new_window_with_label()
            image = ImageTk.PhotoImage(image=Image.fromarray(image))
            label.image = image
            label.configure(image=image)

    def _detect_in_sequence(self) -> None:
        path = fd.askopenfilename()
        if not path:
            logger.error("Sequence path is empty")
            return

        sub_window, label = self._spawn_new_window_with_label()
        video_sequence = self._people_detector.detect_in_sequence(path)
        stop_event = threading.Event()

        def process_sequence():
            while not stop_event.is_set():
                image, count = next(video_sequence)
                image = ImageTk.PhotoImage(image=Image.fromarray(image))
                label.image = image
                label.configure(image=image)
            logger.info(f"Stopped processing video sequence {path}")

        def on_close():
            stop_event.set()
            sub_window.destroy()
        sub_window.protocol("WM_DELETE_WINDOW", on_close)

        thread = threading.Thread(target=process_sequence)
        thread.start()

    def _spawn_new_window_with_label(self):
        sub_window = Toplevel(self._root)
        sub_window.title("Processed image")
        label = tk.Label(sub_window)
        label.pack(side=tk.LEFT)
        return sub_window, label

    async def cleanup(self) -> None:
        if self._ubidots_client is not None:
            await self._ubidots_client.delete_session()
