import sys

import tessy


"""
7. Tessy as a invokable script

This example demonstrates how to write a simple invokable script using tessy and
the "image_to_string" function. 

"""
if __name__ == "__main__":
    lang = None
    image_file = None

    if len(sys.argv) == 2:
        image_file = sys.argv[1]
    elif len(sys.argv) == 4 and sys.argv[1] == "-l":
        lang = sys.argv[2]
        image_file = sys.argv[3]
    else:
        sys.stderr.write("Usage: python 7_tessy_as_script.py [-l lang] image_file")
        exit(0)

    tessy.init()
    print(tessy.image_to_string(image_file, lang=lang))
