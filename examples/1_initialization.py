import platform

import tessy


"""
1. The init function

The init function does two things (in order):
 - Checks if the Tesseract command is valid by trying to start a new process.
   If the command fails, it will try to locate the Tesseract binary.
 - Checks if the Tesseract data directory has been set.

The function will do its best trying to locate the Tesseract binary (if the command fails)
by first looking in the module created cache file (".TESSPATH") then in the registry
(on Windows only).

In fact, this function has been created for Windows in mind since the "tesseract"
binary isn't in the PATH by default.

So, if you are in this case, you can do something like that:
"""
if platform.system().lower() == "windows":
    tessy.init()


"""
This function also works, obviously, on macOS and Linux.

If the "tesseract" command already works and you know where the "tessdata" folder is,
you can completely bypass this function and use "image_to_#" functions directly.

It is strongly recommended (on any OS) to make sure the "tesseract" command is invokable
and add the "TESS_DATAPREFIX" environment variable pointing to your "tessdata" folder.

If, for some reason, you need to set the Tesseract binary path or/and the
"tessdata" folder location manually, you have multiple ways to achieve this:
"""
# Call the "set_command" function to set the binary path
tessy.set_command("path/to/tesseract")
# On Windows it would be something like that:
tessy.set_command("C:\\Program Files\\Tesseract-OCR\\tesseract.exe")

# Call the "set_data_dir" function to set the "tessdata" folder location
tessy.set_data_dir("path/to/tessdata")

# Or use the "configure" function to set one or both of them at the same time:
tessy.configure(command="path/to/tesseract", data_dir="path/to/tessdata")

# You can also pass the "tessdata" folder path using the "config" parameter of any
# "image_to_#" function, like so:
text = tessy.image_to_string([...], config="--tessdata-dir <PATH>")

# If you wish to save the tesseract binary path for further use, you have to pass a
# extra parameter to the "set_command" function:
tessy.set_command("path/to/tesseract", write_cache=True)


"""
Now, next time you want to use tessy again, you can simply call the "init" function
and it will read the cache file and use its content in place of the "tesseract" command.
"""
# Use the "init" function to locate, read and set the cached Tesseract binary path
tessy.init()

# You're now ready to use tessy!


"""
The next example will show how to use tessy to get the text inside an image as a string. 

Less talk, more code.
"""
