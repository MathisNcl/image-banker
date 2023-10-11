![Version](https://img.shields.io/badge/python-3.11-brightgreen)
[![Coverage Status](https://coveralls.io/repos/github/MathisNcl/image-banker/badge.svg?branch=master)](https://coveralls.io/github/MathisNcl/image-banker?branch=master)
![Interrogate Status](assets/interrogate_badge.png)

# ImageBanker: Object Collector & Saver

ImageBanker is a very simple web app for retrieving an object without background.
The main advantage is the ability to detect objects in the photo, so you do not need to take a standardized photo to crop an object - just select it from an old image, for example.

The implementation is not scratch-built: YoloV8 and rembg are used for detection and cropping.

## How do I use it?

Pretty straightforward! Go to this URL, take a photo, choose the object you want to crop, then download the image if you are happy with the crop.

## Special thanks

Thanks to Louis Guichard and his nice [Pictify](https://github.com/louisguichard/pictify/tree/main) for the inspiration.

```bibtex
@software{yolov8_ultralytics,
  author = {Glenn Jocher and Ayush Chaurasia and Jing Qiu},
  title = {Ultralytics YOLOv8},
  version = {8.0.0},
  year = {2023},
  url = {<https://github.com/ultralytics/ultralytics}>,
  orcid = {0000-0001-5950-6979, 0000-0002-7603-6750, 0000-0003-3783-7069},
  license = {AGPL-3.0}
}
```

## ⚗️ Future features

- [ ] Add parameters to remove background
