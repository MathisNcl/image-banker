import numpy as np
import pytest
from PIL import Image
from ultralytics.engine.results import Results

from image_banker.image_client import ImageClient


@pytest.fixture
def orig_shape() -> tuple:
    return (960, 1440)


@pytest.fixture
def dummy_image(orig_shape: tuple) -> Image:
    return Image.fromarray(np.ones(orig_shape))


@pytest.fixture
def result_prediction(orig_shape: tuple) -> Results:
    data: np.ndarray = np.array(
        [[954.69, 641.63, 1075.4, 740.72, 0.90462, 64], [0.54104, 172.05, 270.19, 610.48, 0.8924, 63]], dtype=np.float32
    )
    return Results(
        orig_img=np.ones(orig_shape, dtype=np.uint8), path=None, names={63: "laptop", 64: "mouse"}, boxes=data
    )


@pytest.fixture
def image_client(result_prediction: Results) -> ImageClient:
    class MockYOLO:
        def __init__(self, model_path: str) -> None:
            pass

        def __call__(self, image: Image) -> list:
            return [result_prediction, result_prediction]

    image_client: ImageClient = ImageClient()
    image_client.model = MockYOLO("mock_model")
    return image_client
