# tessy examples

## Summary

### 1. [Initialization](1_initialization.py)

- How, why and when use the **[init](https://github.com/K4rian/tessy#tessyinit)** function.
- Customizing `tesseract` command/binary path and `tessdata` folder location.

### 2. [Image to string](2_image_to_string.py)

How to use the **[image_to_string](https://github.com/K4rian/tessy#tessyimage_to_stringimage-output_formattxt-langnone-confignone)** function to get the text inside an image as a `string`.

### 3. [Image to file](3_image_to_file.py)

How to use the **[image_to_file](https://github.com/K4rian/tessy#tessyimage_to_fileimage-output_filename_basenone-output_formattxt-langnone-confignone)** function to get the text inside an image as a `list` of one or
more file.

### 4. [Image to data](4_image_to_data.py)

How to use the **[image_to_data](https://github.com/K4rian/tessy#tessyimage_to_dataimage-output_formattxt-data_outputstr-langnone-confignone)** function to get the text inside an image as `data`.

### 5. [Words bounding box](5_image_to_data_words_tsv.py)

How to use the **[image_to_data](https://github.com/K4rian/tessy#tessyimage_to_dataimage-output_formattxt-data_outputstr-langnone-confignone)** function to get the `bounding box` of the recognized **words**
inside an image and display the processed image using `OpenCV`.

### 6. [Letters bounding box](6_image_to_data_letters_box.py)

How to use the **[image_to_data](https://github.com/K4rian/tessy#tessyimage_to_dataimage-output_formattxt-data_outputstr-langnone-confignone)** function to get the `bounding box` of the recognized **letters**
inside an image and display the processed image using `OpenCV`.

### 7. [tessy as a script](7_tessy_as_script.py)

How to use tessy as a invokable script.

## Prerequisites to run the examples

- Dev dependencies installed
- A sandbox created with `virtualenv` _(optional but recommended)_

### Setup

- Create the sandbox:

```bash
virtualenv tessy-sandbox
```

- Activate it:

_On macOS/Linux_:

```bash
source /path/to/tessy-sandbox/bin/activate
```

_On Windows_:

```bash
cd tessy-sandbox\Scripts & activate
```

- Create a `workspace` folder to put the project files in:

```bash
mkdir tessy-sandbox\workspace
cd tessy-sandbox\workspace
```

- [Install tessy](https://github.com/K4rian/tessy#installing-tessy)
- Install the dev dependencies using `pip`:

```bash
cd tessy
pip install -r requirements-dev.txt
```

- [Download the examples files](https://github.com/K4rian/tessy/archive/master.zip)
- Run any example script:

```bash
cd examples/
python <script>.py
```
