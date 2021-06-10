import os
import time
import logging
import asyncio
import threading
import tkinter as tk
from typing import Callable
from PIL import Image, ImageTk
from tkinter import Toplevel, filedialog as fd
from concurrent.futures import ThreadPoolExecutor

from .detector import PeopleDetector
from .thread_event_loop import thread_loop
from .client import UbidotsClient, load_ubidots_config


logger = logging.getLogger(__name__)


class App:
    
    def __init__(self, root: tk.Tk):
        self._root = root
        self._people_detector = PeopleDetector()
        self._ubidots_client = UbidotsClient.from_config(load_ubidots_config())
        self._executor = ThreadPoolExecutor(max_workers=5)
        self._add_widgets()

    def _add_widgets(self) -> None:
        self._root.minsize(300, 150)
        self._root.resizable(False, False)
        self._root.title("People detector")
        self._root.eval('tk::PlaceWindow . center')

        tk.Button(text='Process image', command=self._detect_in_image,
                width=15, font='sans 16 bold').pack(pady=20)
        tk.Button(text='Process video', command=self._detect_in_sequence, 
                width=15, font='sans 16 bold').pack(pady=(0, 20))

    def _detect_in_image(self) -> None:
        path = fd.askopenfilename()
        if not path:
            logger.error("Image path is empty")
            return
            
        image, count = self._people_detector.detect_in_image(path)
        if image is not None:
            label = self._spawn_new_window_with_label()
            image = ImageTk.PhotoImage(image=Image.fromarray(image))
            label.configure(image=image)
            label.image = image

            if self._ubidots_client is not None:
                asyncio.run_coroutine_threadsafe(
                    self._ubidots_client.send_request('images', count), 
                    thread_loop
                )

    def _detect_in_sequence(self) -> None:
        path = fd.askopenfilename()
        if not path:
            logger.error("Sequence path is empty")
            return

        stop_event = threading.Event()
        label = self._spawn_new_window_with_label(on_close=stop_event.set)
        video_sequence = self._people_detector.detect_in_sequence(path)
        basename = os.path.basename(path)
        
        def process_sequence():
            start = time.time()
            while not stop_event.is_set():
                image, count = next(video_sequence)
                image = ImageTk.PhotoImage(image=Image.fromarray(image))
                label.configure(image=image)
                label.image = image

                if self._ubidots_client is not None and time.time() - start > 1:
                    start = time.time()
                    asyncio.run_coroutine_threadsafe(
                        self._ubidots_client.send_request(basename, count), 
                        thread_loop
                    )

        self._executor.submit(process_sequence)

    def _spawn_new_window_with_label(self, on_close: Callable = None):
        sub_window = Toplevel(self._root)
        sub_window.title("Processed image")
        sub_window.resizable(False, False)
        label = tk.Label(sub_window)
        label.pack(expand=True)

        def quit():
            if on_close is not None:
                on_close()
            sub_window.destroy()
        sub_window.protocol("WM_DELETE_WINDOW", quit)
        
        return label

    def cleanup(self):
        if self._ubidots_client is not None:
            asyncio.run_coroutine_threadsafe(
                self._ubidots_client.delete_session(), 
                thread_loop
            )
