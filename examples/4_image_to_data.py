import cv2
import wx

import tessy

from PIL import Image as PILImage

from PyQt5.QtGui import QImage


# Inits the module.
# See the first example for more details about this function.
tessy.init()


"""
4. Image to data

This example script demonstrates how to use tessy to get the text inside an image as data.

It is strongly recommended to take a look at the previous examples since this script 
gets straight to the point.

Let's define an image the same way as the previous examples:
"""
# Image file
image = "./images/image1_eng.png"

# Pillow Image
# image = PILImage.open("./images/image1_eng.png")

# OpenCV ndarray
# image = cv2.imread("./images/image1_eng.png")

# PyQt5 Image
# image = QImage("./images/image1_eng.png")

# wxPython Image
# A wx.App object must be created before using any wxPython feature
# wxApp = wx.App()
# image = wx.Image("./images/image1_eng.png", type=wx.BITMAP_TYPE_ANY)


"""
By default, the "image_to_data" function will return the data as a string inside a list.
"""
data = tessy.image_to_data(image)

# Display the data in the console
print("First image data [string]:\n", data[0], "\n")


"""
If we want to get the data in bytes instead of string, we have to use
the "data_output" parameter:
"""
data = tessy.image_to_data(image, data_output=tessy.DataOutput.BYTES)

print("First image data [bytes]:\n", data[0], "\n")


"""
We can also get the data as a dictionary:
"""
data = tessy.image_to_data(image, data_output=tessy.DataOutput.DICT)

print("First image data [dict]:\n", data[0], "\n")


"""
Like the others "image_to_#" functions, we can get multiple output formats as well:
"""
data = tessy.image_to_data(
    image, output_format="txt, tsv, box", data_output=tessy.DataOutput.DICT
)

print("First image data [dict] [txt, tsv and hocr]:\n", data, "\n")


"""
The next example will show how to use the "image_to_data" function to get the 
bounding box of the recognized words inside an image.
"""
