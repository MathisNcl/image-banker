"""Module containing ImageClient used to predict, display and extract objects from an image"""
from typing import Any, Optional

import cv2
import numpy as np
import streamlit as st
from PIL import Image
from rembg import remove
from ultralytics import YOLO
from ultralytics.engine import results

from image_banker import logger, settings


@st.cache_resource
def load_model() -> YOLO:
    """load the Yolo model once then stroe it in cache

    Returns:
        YOLO: Yolo model
    """
    model: YOLO = YOLO(settings.MODEL_PATH)
    logger.info(f"YOLO model loaded from {settings.MODEL_PATH}")
    return model


class ImageClient:
    """Main client to predict and extract object"""

    def __init__(self) -> None:
        """Init"""
        self.model: YOLO = load_model()

    def predict(self, image: Image.Image) -> tuple[dict[str, Any], results.Results]:
        """From a PIL Image, extract all the object with bounding boxes and raw results

        Args:
            image (Image.Image): Image to consider

        Returns:
            tuple[dict[str, Any], results.Results]:
                - dict with "idx_labelobject" template, values are bboxes
                - raw object result from Yolo model
        """
        prediction: list[results.Results] = self.model(image)

        if len(prediction) > 1:
            logger.warning(f"Something went wrong, there are {len(prediction)} results. Only processing the first one.")

        to_numpy: Any = prediction[0].boxes.numpy()

        boxes_per_items: dict[str, Any] = {}
        for i, cls, xyxy in zip(range(len(to_numpy.xyxy)), to_numpy.cls, to_numpy.xyxy):
            boxes_per_items[f"{i}_{prediction[0].names[int(cls)]}"] = [int(coord) for coord in xyxy]

        return boxes_per_items, prediction[0]

    def show_prediction(
        self, prediction: Optional[results.Results] = None, bbox_object: Optional[list[int]] = None, **kwargs: Any
    ) -> Image.Image:
        """From a predicition, plot the bbox into the image and add a special rectangle for the selected object

        Args:
            prediction (Optional[results.Results], optional): Yolo Model result. Defaults to None.
            bbox_object (Optional[list[int]], optional): bbox of the selected object to highlight. Defaults to None.

        Returns:
            Image.Image: New image with bbox printed
        """
        if prediction is not None:
            img: np.ndarray = prediction.plot(**kwargs)
            if bbox_object is not None:
                x1, y1, x2, y2 = bbox_object
                cv2.rectangle(img, (x1, y1), (x2, y2), settings.SELECTED_COLOR, thickness=8)
            return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        logger.error("No prediction yet.")
        raise ValueError("No prediction yet.")

    def extract_obj_bg(self, prediction: results.Results, bbox_object: list[int]) -> Image.Image:
        """Crop the initial image to get only the object and then remove the backgound

        Args:
            prediction (results.Results): Yolo Model result
            bbox_object (list[int]): bbox of the selected object

        Returns:
            Image: Cropped image without background
        """
        x1, y1, x2, y2 = bbox_object
        cropped_img: Image.Image = Image.fromarray(cv2.cvtColor(prediction.orig_img[y1:y2, x1:x2], cv2.COLOR_BGR2RGB))

        logger.info("Starting removal...")
        cropped_img_removed_bg = remove(cropped_img)
        logger.info("Background removed.")

        return cropped_img_removed_bg
