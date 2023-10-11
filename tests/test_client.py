from typing import Any

import numpy as np
import pytest
from PIL import Image
from ultralytics.engine.results import Results

from image_banker.image_client import ImageClient


def test_instanciate(caplog: Any) -> None:
    client: ImageClient = ImageClient()
    assert isinstance(client, ImageClient)
    assert "YOLO model loaded from" in caplog.text


def test_predict(image_client: ImageClient, dummy_image: np.ndarray, caplog: Any) -> None:
    bboxes, result = image_client.predict(dummy_image)

    assert "Something went wrong" in caplog.text
    assert bboxes == {"0_mouse": [954, 641, 1075, 740], "1_laptop": [0, 172, 270, 610]}
    assert isinstance(result, Results)


def test_show_no_prediction(image_client: ImageClient, caplog: Any) -> None:
    with pytest.raises(ValueError):
        image_client.show_prediction()
        "No prediction yet." in caplog.text


def test_show_prediction(image_client: ImageClient, result_prediction: Results, orig_shape: tuple) -> None:
    img = image_client.show_prediction(result_prediction, [954, 641, 1075, 740])

    assert isinstance(img, Image.Image)
    assert img.size == orig_shape[::-1]


def test_extract_obj_bg(image_client: ImageClient, result_prediction: Results, caplog: Any) -> None:
    size = (1075 - 954, 740 - 641)
    img_cropped = image_client.extract_obj_bg(result_prediction, [954, 641, 1075, 740])

    assert isinstance(img_cropped, Image.Image)
    assert img_cropped.size == size

    assert "Starting removal..." in caplog.text
    assert "Background removed." in caplog.text
