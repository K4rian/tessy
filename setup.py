import os
import tessy

from setuptools import setup


README = ""

if os.path.isfile("README.md"):
    with open("README.md") as f:
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
    long_description_content_type="text/markdown",
    keywords="python tesseract ocr",
    packages=["tessy"],
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux,
        "Operating System :: MacOS",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.12",
        "Topic :: Utilities",
    ],
)
