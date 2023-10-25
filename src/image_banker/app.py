"""Front of the Web App"""
from io import BytesIO
from typing import Any, Optional

import streamlit as st
from PIL import Image, ImageOps
from streamlit.runtime.uploaded_file_manager import UploadedFile
from ultralytics.engine.results import Results

from image_banker.image_client import ImageClient

st.set_page_config(page_title="ImageBanker", page_icon="📸")

col1, col2 = st.columns(2)
col1.image("assets/logo.png", width=300)
col2.title(
    "ImageBanker: Object Collector & Saver - *Upload, select and collect your object to create a bank of images*"
)

client: ImageClient = ImageClient()
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


@st.cache_data
def get_objects(image: Image.Image) -> tuple[dict[str, Any], Results]:
    """Predict Yolo model on image

    Args:
        image (Image.Image): Input image

    Returns:
        tuple[dict[str, Any], results.Results]:
            - dict with keys like "idx_labelobject" template, values are bboxes
            - raw object result from Yolo model
    """
    with st.spinner("Wait for it..."):
        bboxes, prediction = client.predict(image)
    return bboxes, prediction


def select_and_show(bboxes: dict[str, Any], prediction: Results) -> None:
    """Retrieve the object cropped without background into the displayed image from dropdown. Downloadable.

    Args:
        bboxes (dict[str, Any]): Bbox of all objects
        prediction (Results): Yolo model prediction
    """
    option: Optional[str] = st.selectbox(
        "Which object do you want to consider?",
        list(bboxes.keys()),
        index=None,
        placeholder="Select object...",
    )

    bbox_selected: Optional[list[int]] = None
    if option is not None:
        bbox_selected = bboxes[option]
    col1, col2 = st.columns(2)

    with st.spinner("Wait for it..."):
        col1.header("Original")
        col1.image(
            client.show_prediction(prediction=prediction, bbox_object=bbox_selected, conf=False), use_column_width=True
        )

        col2.header("Cropped extracted")
        if bbox_selected is not None:
            cropped_img: Image.Image = client.extract_obj_bg(prediction=prediction, bbox_object=bbox_selected)
            col2.image(cropped_img)
            buf: BytesIO = BytesIO()
            cropped_img.save(buf, format="PNG")
            st.download_button(
                label="Download cropped image",
                data=buf.getvalue(),
                file_name=f"extracted_{option}.png",
                mime="image/png",
            )


uploaded_img: UploadedFile | None = st.file_uploader("Take a photo of desired object", type=["png", "jpg", "jpeg"])

if uploaded_img:
    image: Image.Image = ImageOps.exif_transpose(Image.open(uploaded_img))
    bboxes, prediction = get_objects(image)
    select_and_show(bboxes, prediction)
