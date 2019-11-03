import cv2
import wx

import tessy

from PIL import Image as PILImage

from PyQt5.QtGui import QImage


# Inits the module.
# See the first example for more details about this function.
tessy.init()


"""
2. Image to string

This example script demonstrates how to use tessy to get the text inside an image as
a string.

Let's define an image in each supported way:
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
Since we have an image to work with, let's try to get the text inside the
image using the "image_to_string" function from tessy:
"""
# Let's pass the image without additional parameters for now
text = tessy.image_to_string(image)

# Display the text in the console
print("First image text:\n", text, "\n")


"""
If the text isn't in English (or mixed), we can also specify one or more additional
language:
"""
# Define a new image containing some German text
image2 = "./images/image2_eng+deu.png"

# Use the German language instead of English
text = tessy.image_to_string(image2, lang=tessy.Lang.GERMAN)
print("Second image text (German):\n", text, "\n")

# Since the image also contains some English text so we could specify both languages.
# NOTE: Languages order matter: in the example image the English text comes first.
text = tessy.image_to_string(image2, lang=[tessy.Lang.ENGLISH, tessy.Lang.GERMAN])
print("Second image text (English+German):\n", text, "\n")


"""
Multiple output formats are also possible:
"""
# Gets the text data string in txt and tsv format
text_data = tessy.image_to_string(image2, output_format="txt, tsv")

# Split the text data string using the default tessy content separator
(text, tsv) = text_data.split(tessy.content_sep())
print(
    "-------------\n"
    "Second image [text]:\n"
    "{0}\n"
    "-------------\n"
    "Second image [tsv]:\n"
    "{1}\n".format(text, tsv)
)


"""
To handle multiple files at once, we can specify a text file (.txt) containing
one image (absolute path) per line.

Let's say we have a text file called "all-images.txt" in "/home/tess/images",
we can add the following examples images inside it:

/home/tess/images/image-1.png
/home/tess/images/image-2.png
/home/tess/images/image-3.png

Once the file is saved, we can use it as an image with tessy:

images_list = "/home/tess/images/all-images.txt"
text = tessy.image_to_string(images_list)
print(text)
"""


"""
The next example will show how to use tessy to get the text inside an image as a list 
of one or more files.
"""
