import cv2
import wx

import tessy

from PIL import Image as PILImage

from PyQt5.QtGui import QImage


# Inits the module.
# See the first example for more details about this function.
tessy.init()


"""
3. Image to file

This example script demonstrates how to use tessy to get the text inside an image
as a list of one or more files.

It is strongly recommended to take a look at the previous example since this script
gets straight to the point.

Let's define an image the same way as the previous example:
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
Now we can call "image_to_file" function to get a list containing a .txt file (default) 
with the extracted text inside it.
"""
txt_file = tessy.image_to_file(image)

# Display the file path in the console
print("First image txt file [path]:\n", txt_file[0], "\n")

# Read its content and display it
try:
    with open(txt_file[0], "r") as f:
        print("First image txt file [content]:\n", f.read().strip(), "\n")
except IOError as e:
    print(
        "ERROR: Could not read the file '{0}', I/O Error ({1}): {2}".format(
            txt_file[0], e.errno, e.strerror
        )
    )


"""
Like the "image_to_string" function we can get multiple output formats:
"""
# Define a new image containing some German text
image2 = "./images/image2_eng+deu.png"

# Gets the extracted text in txt, tsv and pdf formats
files_list = tessy.image_to_file(
    image2, output_format="txt, tsv, pdf", lang=[tessy.Lang.ENGLISH, tessy.Lang.GERMAN]
)

# Display the files list in the console
print("Second image files list [txt, tsv and pdf]:\n", "\n".join(files_list), "\n")


"""
We can also specify a custom file name for our files using the "output_filename_base" 
parameter. The "output_filename_base" parameter is used as a "template" file name 
(without extension). See the documentation for more information.
"""
# Same as before but using a custom file name pointing to the current directory
files_list = tessy.image_to_file(
    image2,
    output_filename_base="./3-second-image-data",
    output_format="txt, tsv, pdf",
    lang=[tessy.Lang.ENGLISH, tessy.Lang.GERMAN],
)

# Should output:
#  ./3-second-image-data.txt
#  ./3-second-image-data.tsv
#  ./3-second-image-data.pdf
print(
    "Second image files list [txt, tsv and pdf] in the current directory:\n",
    "\n".join(files_list),
    "\n",
)


"""
Once we're done with the files, we can tell tessy to clean (delete) all of them.
NOTE: Any file outside the temporary directory won't be deleted.
"""
tessy.clear_temp()


"""
The next example will show how to use tessy to get the text inside an image as data.
"""
