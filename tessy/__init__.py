"""
tessy
=====

__tessy__ is a Python wrapper for [Google's Tesseract-OCR](https://github.com/tesseract-ocr/tesseract), 
an optical character recognition engine used to *detect and extract* text data from various image file formats.

---
<p align="center">
  <a href="#features">Features</a> &bull; <a href="#prerequisites">Prerequisites</a> &bull; <a href="#installing-tesseract">Installing Tesseract</a><br> 
  <a href="#installing-tessy">Installing tessy</a> &bull; <a href="#basic-usage">Basic Usage</a> &bull; <a href="#api">Documentation</a> &bull; <a href="#license">License</a>
</p>

## Features
- No initial dependencies beside [Tesseract](https://github.com/tesseract-ocr/tesseract).
- Supports input image in `PNG`, `JPG`, `JPEG`, `GIF`, `TIF` and `BMP` format.
- Supports multiple input images via text file *(.txt)*.
- Supports image objects from: 
  * [Pillow](https://github.com/python-pillow/Pillow) *(Image)*
  * [wxPython](https://github.com/wxWidgets/wxPython) *(wx.Image)*
  * [PyQt4](https://www.riverbankcomputing.com/software/pyqt/download)/
    [PyQt5](https://www.riverbankcomputing.com/software/pyqt/download5)/
    [PySide](https://github.com/pyside/pyside-setup) *(QImage)*
  * [OpenCV](https://github.com/skvark/opencv-python) *(ndarray)*
- Dynamically detect and import the corresponding image module on runtime.
- Supports `txt`, `box`, `pdf`, `hocr`, `tsv` and `osd` as output file format.
- Supports multiple output format.
- Can convert any raw output data to `string`, `bytes` or `dict` *(except pdf)*.
- Works on macOS, Linux and Windows.
- Well [documented](@@#api).

## Prerequisites
- Python 3.12+
- [Google's Tesseract-OCR](https://github.com/tesseract-ocr/tesseract) 5.2.x+
*(5.3.x+ on Windows recommended)*

## Installing Tesseract
Tesseract comes in two parts: The engine itself and the training data for each supported language.

### Installation on macOS
- Install both Tesseract and the training data:
```bash
brew install tesseract
```

### Installation on Linux (Debian/Ubuntu)
The package is generally called `tesseract` or `tesseract-ocr`.

- Install Tesseract:
```bash
sudo apt install tesseract-ocr
```
- Install an additional language:
```bash
sudo apt install tesseract-ocr-{LANG_CODE}
```
- *(example)* Install the Finish language:
```bash
sudo apt install tesseract-ocr-fin
```
- All languages can be installed at once:
```bash
sudo apt install tesseract-ocr-all
```

*It is highly recommended to browse the [Tesseract-OCR's wiki](https://github.com/tesseract-ocr/tesseract/wiki) 
to get more informations about other Linux distributions and languages installation.*

### Installation on Windows
Installers for Windows are available on [Tesseract at UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki) 
*(version 5.0.x+ recommended)*.

### Post-install
After the installation, it is strongly recommended to:
- Make sure the `tesseract` command is invokable.
  - This is generally not the case on Windows where you have to add the tesseract installation directory to your `PATH`.
- Set the `TESSDATA_PREFIX` environment variable pointing to your `tessdata` directory
*(`<tesseract_dir>\\tessdata` on Windows, variable on macOS/Linux)*.

## Installing tessy
__Install the [PyPI package](https://pypi.org/project/tessy/)__:
```bash
sudo pip install tessy
```
__or clone the repository__:
```bash
git clone @@
```

## Basic Usage
```python
import tessy

# Inits the module (optional - see the examples)
tessy.init()

# Path to an image
image = "/home/tess/images/image-1.png"

# Gets the text from the image
text = tessy.image_to_string(image)

# Shows the text in the console
print(text)
```

Check out the __[examples](examples/README.md)__ for more advanced usages and the __[documentation](@@#api)__ to see what features are available.
"""
from ._tessy import (
    Lang,
    DataOutput,
    command,
    set_command,
    data_dir,
    set_data_dir,
    content_sep,
    set_content_sep,
    configure,
    init,
    image_to_file,
    image_to_data,
    image_to_string,
    locate,
    locate_data,
    run,
    runnable,
    start,
    tesseract_version,
    clear_cache,
    clear_temp,
    sv_to_dict,
    boxes_to_dict,
    hocr_to_dict,
    osd_to_dict,
)

VERSION = "0.5.2"