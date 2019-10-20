import os
import tessy

from setuptools import setup


README = ""

if os.path.isfile("README.rst"):
    with open("README.rst") as f:
        README = f.read()

setup(
    name="tessy",
    version=tessy.VERSION,
    author="K4rian",
    author_email="contact@k4rian.com",
    url="https://github.com/k4rian/tessy",
    license="MIT",
    description="A Python wrapper for Tesseract-OCR.",
    long_description=README,
    keywords="tesseract",
    packages=["tessy"],
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.4",
        "Topic :: Utilities",
    ],
)
