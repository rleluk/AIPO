import os
import cv2
import logging
import imutils
import numpy as np
from typing import Tuple
from imutils.object_detection import non_max_suppression


logger = logging.getLogger(__name__)


class PeopleDetector:

    class InvalidPath(Exception):

        def __init__(self, path: str):
            self._path = path

        def __str__(self) -> str:
            return f"Couldn't load {self._path}"

    def __init__(self, ):
        self._hogcv = cv2.HOGDescriptor()
        self._hogcv.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    def detect_in_sequence(self, path: str) -> Tuple[np.array, int]:
        video = cv2.VideoCapture(path)
        if video is None:
            raise PeopleDetector.InvalidPath(path)

        filename = os.path.basename(path)    
        
        while True:
            _, frame = video.read()
            result, count = self._detect_people(frame)
            logger.debug(f"Number of detected people in video '{filename}': {count}")
            yield result, count
            
    def detect_in_image(self, path: str) -> Tuple[np.array, int]:
        image = cv2.imread(path)
        if image is None:
            raise PeopleDetector.InvalidPath(path)

        result, count = self._detect_people(image)
        filename = os.path.basename(path)    
        logger.debug(f"Number of detected people in image '{filename}': {count}")
        return result, count
        
    def _detect_people(self, image: np.array) -> Tuple[np.array, int]:
        image = imutils.resize(image, width=min(600, image.shape[1]))

        rects, _ = self._hogcv.detectMultiScale(
            image, winStride=(4, 4), padding=(8, 8), scale=1.05
        )

        rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
        result = non_max_suppression(rects, probs=None, overlapThresh=0.65)

        for (x_1, y_1, x_2, y_2) in result:
            cv2.rectangle(image, (x_1, y_1), (x_2, y_2), (255, 0, 255), 2)
        
        return cv2.cvtColor(image, cv2.COLOR_BGR2RGB), len(result)