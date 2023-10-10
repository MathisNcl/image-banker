import sys
from pathlib import Path
from typing import Optional, cast

from pydantic import ConfigDict, ValidationInfo, field_validator
from pydantic_settings import BaseSettings

PACKAGE_DIR: Path = Path(cast(str, sys.modules["image_banker"].__file__)).parent
BASE_DIR: Path = PACKAGE_DIR.parent.parent if PACKAGE_DIR.parent.name == "src" else PACKAGE_DIR


class Settings(BaseSettings):
    MODEL_NAME: str = "yolov8s.pt"
    MODEL_FOLDER: Path = BASE_DIR / "model"
    MODEL_PATH: Optional[str] = None

    SELECTED_COLOR: tuple = (255, 0, 0)

    @field_validator("MODEL_PATH", mode="after")
    def get_model_path(cls, v: Optional[str], info: ValidationInfo) -> str:
        return v or f"{info.data.get('MODEL_FOLDER')}/{info.data.get('MODEL_NAME')}"

    model_config = ConfigDict(env_file=BASE_DIR / ".env", extra="ignore")
