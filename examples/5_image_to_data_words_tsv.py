import cv2

import tessy


# Inits the module.
# See the first example for more details about this function.
tessy.init()


"""
5. Image to data - Words bounding box

This example script demonstrates how to use the "image_to_data" function to get the 
bounding box of the recognized words inside an image.

It is strongly recommended to take a look at the previous examples since this script 
gets straight to the point.

For this example we're going to use OpenCV to be able to show the result on screen.
"""
# Gets the image as a NumPy ndarray
image = cv2.imread("./images/image1_eng.png", cv2.IMREAD_UNCHANGED)


"""
Gets the image data in tsv format as a dictionary:
"""
data = tessy.image_to_data(
    image, output_format="tsv", data_output=tessy.DataOutput.DICT
)


"""
Since the "image_to_#" functions don't alter the given image and may contain 
transparency, we need to get rid of the alpha channel and replace it 
with white background before drawing on top of the image:
"""
if len(image.shape) > 2 and image.shape[2] == 4:
    (rt, th) = cv2.threshold(image[:, :, 3], 254, 255, cv2.THRESH_BINARY)
    image = cv2.bitwise_not(cv2.bitwise_not(image[:, :, :3], mask=th))


"""
Let's use the data to draw the boxes around each word:
"""
# Define the box data with a more friendly name
box_data = data[0]

# Define the box data length
box_data_len = len(box_data["level"])

for i in range(box_data_len):
    # If we got a word...
    if box_data["text"][i].strip():
        # Define the box coordinates
        (x, y, w, h) = (
            box_data["left"][i],
            box_data["top"][i],
            box_data["width"][i],
            box_data["height"][i],
        )
        # Draw the box around the word using the green color with a
        # thickness of 2 pixels for the lines
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)


"""
Show the result on screen and wait until the window is manually closed:
"""
cv2.imshow("Words bounding box", image)
cv2.waitKey(0)


"""
The next example will show how to use the "image_to_data" function to get the 
bounding box around the letters of the recognized text inside an image.
"""
