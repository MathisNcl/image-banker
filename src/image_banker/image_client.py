from typing import Any, Optional

import cv2
import numpy as np
from PIL import Image
from rembg import remove
from ultralytics import YOLO
from ultralytics.engine import results

from image_banker import logger, settings


class ImageClient:
    def __init__(self) -> None:
        self.model = YOLO(settings.MODEL_PATH)
        # FIXME: not sure needed
        if isinstance(self.model, YOLO):
            raise TypeError("Could not load YOLO model, did you forget to set MODEL_PATH ?")
        logger.info(f"YOLO model loaded from {settings.MODEL_PATH}")

    def predict(self, image: Image) -> dict[str, Any]:
        prediction: list[results.Results] = self.model(image)

        if len(prediction) > 1:
            logger.warning(f"Something went wrong, there are {len(prediction)} results. Only processing the first one.")

        self.prediction: results.Results = prediction[0]

        to_numpy: Any = self.prediction.boxes.numpy()

        boxes_per_items: dict[str, Any] = {}
        for cls, xyxy in zip(to_numpy.cls, to_numpy.xyxy):
            boxes_per_items[self.prediction.names[int(cls)]] = [int(coord) for coord in xyxy]

        return boxes_per_items

    def show_prediction(self, bbox_object: Optional[list[int]] = None, **kwargs: Any) -> Image:
        if self.prediction is not None:
            img: np.ndarray = self.prediction.plot(**kwargs)
            if bbox_object is not None:
                x1, y1, x2, y2 = bbox_object
                cv2.rectangle(img, (x1, y1), (x2, y2), settings.SELECTED_COLOR, thickness=8)
            return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        logger.error("No prediction yet.")
        raise ValueError("No prediction yet.")

    def extract_obj_bg(self, bbox_object: list[int]) -> Image:
        x1, y1, x2, y2 = bbox_object
        cropped_img = Image.fromarray(cv2.cvtColor(self.prediction.orig_img[y1:y2, x1:x2], cv2.COLOR_BGR2RGB))

        logger.info("Starting removal...")
        cropped_img_removed_bg = remove(cropped_img)
        logger.info("Background removed.")

        return cropped_img_removed_bg
