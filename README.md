tessy
=====

__tessy__ is a Python wrapper for 
[Google's Tesseract-OCR](https://github.com/tesseract-ocr/tesseract), 
an optical character recognition engine used to *detect and extract* text data from 
various image file formats.


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
- Well [documented](https://github.com/k4rian/tessy#api).


## Installation

### Prerequisites

- Python 3.4+
- [Google's Tesseract-OCR](https://github.com/tesseract-ocr/tesseract) 3.5.x+
*(5.0.x+ on Windows recommended)*


## Installing Tesseract

Tesseract comes in two parts: The engine itself and the training data for
each supported language.

__>Installation on macOS__ (via [Homebrew](https://brew.sh/))

- Install both Tesseract and the training data:
```
brew install tesseract
```

__>Installation on Linux__ (Debian/Ubuntu)

The package is generally called `tesseract` or `tesseract-ocr`.

- Install Tesseract:
```
sudo apt-get install tesseract-ocr
```
- Install an additional language:
```
sudo apt-get install tesseract-ocr-<langcode>
```
- *(example)* Install the Finish language:
```
sudo apt-get install tesseract-ocr-fin
```
- You can also install all languages at once by running:
```
sudo apt-get install tesseract-ocr-all
```

*It is strongly recommended to browse the 
[Tesseract-OCR's wiki](https://github.com/tesseract-ocr/tesseract/wiki) 
to get more informations about other Linux distributions and languages installation.*

__>Installation on Windows__

Both 32bit and 64bit installers for Windows are available from 
[Tesseract at UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki)
*(version 5.0.x+ recommended)*.


__>Post-install it is strongly recommended to__:
- Makes sure the `tesseract` command is invokable.
  - This is generally not the case on Windows where you have to add the tesseract
  installation directory to your `PATH`.
- Sets the `TESSDATA_PREFIX` environment variable pointing to your `tessdata` directory
*(`<tesseract_dir>\tessdata` on Windows, variable on macOS/Linux)*.


## Installing tessy

__>Install the [PyPI package](https://pypi.org/project/tessy/)__:
```
sudo pip install tessy
```

__>or clone the repository__:
```
git clone https://github.com/k4rian/tessy
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

Check out the __[examples](/examples)__ for more advanced usages and the 
__[documentation](https://github.com/k4rian/tessy#api)__ to see what features are available.
# API
#### Table of Contents
- [tessy.**Lang**](#tessylang) 
- [tessy.**command**](#tessycommand) 
- [tessy.**set_command**](#tessyset_commandcmd-check_runnablefalse-write_cachefalse) 
- [tessy.**data_dir**](#tessydata_dir) 
- [tessy.**set_data_dir**](#tessyset_data_dirdatadir-update_envtrue) 
- [tessy.**content_sep**](#tessycontent_sep) 
- [tessy.**set_content_sep**](#tessyset_content_sepsep) 
- [tessy.**configure**](#tessyconfigurekw) 
- [tessy.**init**](#tessyinit) 
- [tessy.**image_to_file**](#tessyimage_to_fileimage-output_filename_basenone-output_formattxt-langnone-confignone) 
- [tessy.**image_to_data**](#tessyimage_to_dataimage-output_formattxt-data_outputstr-langnone-confignone) 
- [tessy.**image_to_string**](#tessyimage_to_stringimage-output_formattxt-langnone-confignone) 
- [tessy.**locate**](#tessylocate) 
- [tessy.**locate_data**](#tessylocate_data) 
- [tessy.**run**](#tessyrunparametersnone-silentfalse) 
- [tessy.**runnable**](#tessyrunnable) 
- [tessy.**start**](#tessystartparametersnone-silentfalse) *(alias)*
- [tessy.**tesseract_version**](#tessytesseract_version) 
- [tessy.**clear_cache**](#tessyclear_cache) 
- [tessy.**clear_temp**](#tessyclear_tempremove_alltrue) 
- [tessy.**sv_to_dict**](#tessysv_to_dictsv_data-cell_delimitert) 
- [tessy.**boxes_to_dict**](#tessyboxes_to_dictboxes_data) 
- [tessy.**hocr_to_dict**](#tessyhocr_to_dicthocr_data) 
- [tessy.**osd_to_dict**](#tessyosd_to_dictosd_data) 

## tessy.Lang
`TessyLang` enumerates all supported languages by `Tesseract`.

This class can only be accessed through the `tessy.Lang` variable.
### TessyLang.all()
Returns a key-value pair list of all available languages.
### TessyLang.contains(value)
Returns `True` if the given value equals any existing language value.
### TessyLang.join(*args)
Returns an string in which each given languages have been joined by 
the `+` separator.
### TessyLang.print_all()
Prints the key-value pairs of all available languages in the console.
### TessyLang.AFRIKAANS
> = "afr"
### TessyLang.AMHARIC
> = "amh"
### TessyLang.ARABIC
> = "ara"
### TessyLang.ASSAMESE
> = "asm"
### TessyLang.AZERBAIJANI
> = "aze"
### TessyLang.AZERBAIJANI_CYRILLIC
> = "aze_cyrl"
### TessyLang.BELARUSIAN
> = "bel"
### TessyLang.BENGALI
> = "ben"
### TessyLang.TIBETAN
> = "bod"
### TessyLang.BOSNIAN
> = "bos"
### TessyLang.BULGARIAN
> = "bul"
### TessyLang.CATALAN_VALENCIAN
> = "cat"
### TessyLang.CEBUANO
> = "ceb"
### TessyLang.CZECH
> = "ces"
### TessyLang.CHINESE_SIMPLIFIED
> = "chi_sim"
### TessyLang.CHINESE_TRADITIONAL
> = "chi_tra"
### TessyLang.CHEROKEE
> = "chr"
### TessyLang.WELSH
> = "cym"
### TessyLang.DANISH
> = "dan"
### TessyLang.GERMAN
> = "deu"
### TessyLang.DZONGKHA
> = "dzo"
### TessyLang.GREEK_MODERN
> = "ell"
### TessyLang.ENGLISH
> = "eng"
### TessyLang.ENGLISH_MIDDLE
> = "enm"
### TessyLang.ESPERANTO
> = "epo"
### TessyLang.ESTONIAN
> = "est"
### TessyLang.BASQUE
> = "eus"
### TessyLang.PERSIAN
> = "fas"
### TessyLang.FINNISH
> = "fin"
### TessyLang.FRENCH
> = "fra"
### TessyLang.FRANKISH
> = "frk"
### TessyLang.FRENCH_MIDDLE
> = "frm"
### TessyLang.IRISH
> = "gle"
### TessyLang.GALICIAN
> = "glg"
### TessyLang.GREEK_ANCIENT
> = "grc"
### TessyLang.GUJARATI
> = "guj"
### TessyLang.HAITIAN
> = "hat"
### TessyLang.HAITIAN_CREOLE
> = "hat"
### TessyLang.HEBREW
> = "heb"
### TessyLang.HINDI
> = "hin"
### TessyLang.CROATIAN
> = "hrv"
### TessyLang.HUNGARIAN
> = "hun"
### TessyLang.INUKTITUT
> = "iku"
### TessyLang.INDONESIAN
> = "ind"
### TessyLang.ICELANDIC
> = "isl"
### TessyLang.ITALIAN
> = "ita"
### TessyLang.ITALIAN_OLD
> = "ita_old"
### TessyLang.JAVANESE
> = "jav"
### TessyLang.JAPANESE
> = "jpn"
### TessyLang.KANNADA
> = "kan"
### TessyLang.GEORGIAN
> = "kat"
### TessyLang.GEORGIAN_OLD
> = "kat_old"
### TessyLang.KAZAKH
> = "kaz"
### TessyLang.CENTRAL_KHMER
> = "khm"
### TessyLang.KIRGHIZ
> = "kir"
### TessyLang.KYRGYZ
> = "kir"
### TessyLang.KOREAN
> = "kor"
### TessyLang.KURDISH
> = "kur"
### TessyLang.LAO
> = "lao"
### TessyLang.LATIN
> = "lat"
### TessyLang.LATVIAN
> = "lav"
### TessyLang.LITHUANIAN
> = "lit"
### TessyLang.MALAYALAM
> = "mal"
### TessyLang.MARATHI
> = "mar"
### TessyLang.MACEDONIAN
> = "mkd"
### TessyLang.MALTESE
> = "mlt"
### TessyLang.MALAY
> = "msa"
### TessyLang.BURMESE
> = "mya"
### TessyLang.NEPALI
> = "nep"
### TessyLang.DUTCH
> = "nld"
### TessyLang.FLEMISH
> = "nld"
### TessyLang.NORWEGIAN
> = "nor"
### TessyLang.ORIYA
> = "ori"
### TessyLang.PANJABI
> = "pan"
### TessyLang.PUNJABI
> = "pan"
### TessyLang.POLISH
> = "pol"
### TessyLang.PORTUGUESE
> = "por"
### TessyLang.PUSHTO
> = "pus"
### TessyLang.PASHTO
> = "pus"
### TessyLang.ROMANIAN
> = "ron"
### TessyLang.MOLDAVIAN
> = "ron"
### TessyLang.MOLDOVAN
> = "ron"
### TessyLang.RUSSIAN
> = "rus"
### TessyLang.SANSKRIT
> = "san"
### TessyLang.SINHALA
> = "sin"
### TessyLang.SINHALESE
> = "sin"
### TessyLang.SLOVAK
> = "slk"
### TessyLang.SLOVENIAN
> = "slv"
### TessyLang.SPANISH
> = "spa"
### TessyLang.CASTILIAN
> = "spa"
### TessyLang.SPANISH_OLD
> = "spa_old"
### TessyLang.CASTILIAN_OLD
> = "spa_old"
### TessyLang.ALBANIAN
> = "sqi"
### TessyLang.SERBIAN
> = "srp"
### TessyLang.SERBIAN_LATIN
> = "srp_latn"
### TessyLang.SWAHILI
> = "swa"
### TessyLang.SWEDISH
> = "swe"
### TessyLang.SYRIAC
> = "syr"
### TessyLang.TAMIL
> = "tam"
### TessyLang.TELUGU
> = "tel"
### TessyLang.TAJIK
> = "tgk"
### TessyLang.TAGALOG
> = "tgl"
### TessyLang.THAI
> = "tha"
### TessyLang.TIGRINYA
> = "tir"
### TessyLang.TURKISH
> = "tur"
### TessyLang.UIGHUR
> = "uig"
### TessyLang.UYGHUR
> = "uig"
### TessyLang.UKRAINIAN
> = "ukr"
### TessyLang.URDU
> = "urd"
### TessyLang.UZBEK
> = "uzb"
### TessyLang.UZBEK_CYRILLIC
> = "uzb_cyrl"
### TessyLang.VIETNAMESE
> = "vie"
### TessyLang.YIDDISH
> = "yid"
## tessy.command()
Returns the `Tesseract` command.

Returned value can be either the command itself or the binary path.

*Default:* `tesseract`
## tessy.set_command(cmd, check_runnable=False, write_cache=False)
Sets the `Tesseract` command.

> If __`check_runnable`__ is set to `True`, the function will check if the given command 
> is runnable by starting a new process.

> If __`write_cache`__ is set to `True`, the given command will be stored in a special 
> file located in the temporary directory to helps `tessy` to locate Tesseract when the 
> __[init](https://github.com/k4rian/tessy#tessyinit)__ function is called.
## tessy.data_dir()
Returns the `Tesseract` data directory.

*Default:* `None`
## tessy.set_data_dir(datadir, update_env=True)
Sets the location of the `Tesseract` data directory.

> `datadir` must be an absolute path.

> If __`update_env`__ is set to `True`, the `TESSDATA_PREFIX` environment variable
> will be set using __`datadir`__'s value.
## tessy.content_sep()
Returns the content separator. 

> The content separator is used as delimiter when multiple string are joined  
> in the functions __[image_to_string](https://github.com/k4rian/tessy#tessyimage_to_stringimage-output_formattxt-langnone-confignone)__ and
> __[image_to_data](https://github.com/k4rian/tessy#tessyimage_to_dataimage-output_formattxt-data_outputstr-langnone-confignone)__.

*Default:* `||||`
## tessy.set_content_sep(sep)
Sets the content separator.
## tessy.configure(**kw)
All-in-one function to set the `command`, the `data directory` or/and the 
`content separator`.

*Supported keywords*: `command`, `data_dir`, `content_sep`

*Example usage*:                         
```python
configure(command="tesseract", content_sep="~")
```

*Example usage with packed parameters as list/tuple*:           
```python
configure(command=("tesseract", True), data_dir=("/home/tess/data", True))
```

See __[set_command](https://github.com/k4rian/tessy#tessyset_commandcmd-check_runnablefalse-write_cachefalse)__, __[set_data_dir](https://github.com/k4rian/tessy#tessyset_data_dirdatadir-update_envtrue)__ 
and __[set_content_sep](https://github.com/k4rian/tessy#tessyset_content_sepsep)__ functions documentation for 
more details about the parameters.
## tessy.init()
Inits the module by performing some verifications.

- Checks if the `Tesseract` command is valid by trying to start a new process using
the `runnable` function. If the command fails, it will try to locate the `Tesseract` 
binary by calling the __[locate](https://github.com/k4rian/tessy#tessylocate)__ function.
- Checks if the `Tesseract` data directory has been set by calling the 
__[locate_data](https://github.com/k4rian/tessy#tessylocate_data)__ function.
## tessy.image_to_file(image, output_filename_base=None, output_format='txt', lang=None, config=None)
Extracts any text from the given image and return a list containing a unique file 
name for each specified format.

> __`image`__ can be either:
> - an `string` containing the absolute path to an image or a text file containing
> multiple absolute image paths.
> - an Pillow `Image`.
> - an wxPython `Image`.
> - an PyQt4/PyQt5/PySide `QImage`.
> - an OpenCV `NumPy ndarray`.

> __`output_filename_base`__ may contain the file name __without extension__ used 
> as reference for any output file generated by Tesseract.
>
> *e.g.*: If `/home/tess/myimage` is given, the `/home/tess` directory may contain 
> the files `myimage.txt`, `myimage.tsv`, etc.
>
> If __`output_filename_base`__ is set to `None`, all file(s) will be using the same 
> random name as reference and will be saved in the OS's temporary directory.

> __`output_format`__ contains one or more output format(s) who will be processed by 
> `Tesseract`.
>
> *Supported formats*: `txt`, `box`, `pdf`, `hocr`, `tsv`, `osd`
>
> __`output_format`__ can be either:
> - an `string` containing one or more format(s) delimited by a comma `,`
> - a `list`/`tuple` of `string`
>
> *e.g.*: `"txt"`, `"txt, tsv, box"`, `("pdf", "hocr")`, `["txt", "box"]`
>
> __*Note*: If the `osd` format is present, `Tesseract` will only process this 
> format and, thus, return a single file even if multiple formats are provided
> in `output_format`__.

> __`lang`__ may contain one or more supported language(s).
>
> __`lang`__ can be either:
> - an `string` containing one or more languages delimited by a plus sign `+`
> - a `list`/`tuple` of `string`
> - a `TessyLang` enum
> - a `list`/`tuple` of `TessyLang` enums
>           
> *e.g.*: `"deu"`, `"eng+fra"`, `["eng", "fra", "deu"]`, `tessy.Lang.CZECH`, 
> `[tessy.Lang.DANISH, tessy.Lang.TURKISH]`
>
> If __`lang`__ is set to `None`, `Tesseract` will process the image using the 
> English language value (`"eng"`) as default.
>
> __Check the [TessyLang](https://github.com/k4rian/tessy#tessylang) class documentation to get the list
> of all supported languages__.

> __`config`__ may contain extra parameter(s) added to the `Tesseract` command.
>
> __`config`__ must be an string and each parameter must be delimited by a space.
>
> *e.g.*: `"--oem 0 --psm 6"`
## tessy.image_to_data(image, output_format='txt', data_output='str', lang=None, config=None)
Extracts any text from the given image and return a list containing the converted 
data for each specified format.

> __`data_output`__ specifies the type of output data to be returned for each
> given format in __`output_format`__.
>
> *Supported values*: `DataOutput.BYTES`, `DataOutput.STRING`, `DataOutput.DICT`
>
> *Default:* `DataOutput.STRING`

See __[image_to_file](https://github.com/k4rian/tessy#tessyimage_to_fileimage-output_filename_basenone-output_formattxt-langnone-confignone)__ documentation for more details about 
__`image`__, __`output_format`__,  __`lang`__ and __`config`__ parameters.

*Note*: `pdf` output format isn't supported by this function.
## tessy.image_to_string(image, output_format='txt', lang=None, config=None)
Extracts any text from the given image and return the data as string for each 
specified format.

See __[image_to_file](https://github.com/k4rian/tessy#tessyimage_to_fileimage-output_filename_basenone-output_formattxt-langnone-confignone)__ documentation for more details about 
__`image`__, __`output_format`__,  __`lang`__ and __`config`__ parameters.

*Note*: `pdf` output format isn't supported by this function.
## tessy.locate()
Tries to locate the Tesseract binary and returns its path if found.

- Checks if the cache file (`.TESSPATH`) is present inside the temporary directory.   
If the file is found, its content is read and returned as an string.
- (__Windows only__) Tries to read the Tesseract installation directory in the
registry. The registry entry only exists if Tesseract has been previously installed
using the Windows precompiled setups. If the Tesseract executable is located, its
path is returned as an string.
## tessy.locate_data()
Tries to locate the Tesseract data directory and returns its path if found.

- Checks if the `TESSDATA_PREFIX` environement variable has been set and return
its value.
- Tries to read the Tesseract installation directory in the
registry. The registry entry only exists if Tesseract has been previously installed
using any Windows precompiled setups. If the Tesseract executable is located, its
path is returned as an string.
## tessy.run(parameters=None, silent=False)
Run Tesseract with the given parameters and return the output as tuple.

> __`parameters`__ contains the parameters to pass to Tesseract as string.
>
> *e.g.*: `"C:\my-image.png C:\my-image -l eng+deu box"`

> If __`silent`__ is set to `True`, warning messages won't be logged.

*Returned values* (3): `status` (returncode/int), `output` (stoutdata/string), 
`err_string` (sterrdata/string)
## tessy.runnable()
Returns `True` if the Tesseract's process can be started.
## tessy.start(parameters=None, silent=False)
Alias of __[run](https://github.com/k4rian/tessy#tessyrunparametersnone-silentfalse)__
## tessy.tesseract_version()
Returns the `LooseVersion` representation of Tesseract's version.
## tessy.clear_cache()
Tries to remove the `.TESSPATH` cache file and return `True` if successfully deleted.
## tessy.clear_temp(remove_all=True)
Removes temporary files created by Tesseract *(excluding the cache file)*.

> If __`remove_all`__ is set to `True`, all temporary files will be deleted.      
> Otherwise, only temporary files created during execution will be deleted.
## tessy.sv_to_dict(sv_data, cell_delimiter='\t')
Converts and return the given `separated-values` raw data as a dictionary.

> __`sv_data`__ must contain a header row.

*SV data sample (separated by a comma)*:
```
head1,head2,head3,head4
A1,A2,A3,A4
B1,B2,B3,B4
C1,C2,C3,C4
```

*Output*: 
```json
{
    "head1": [
        "A1", "B1", "C1"
    ],
    "head2": [
        "A2", "B2", "C2"
    ],
    [...]
}
```
## tessy.boxes_to_dict(boxes_data)
Converts and return the given `boxes` data as a dictionary.

> __`boxes_data`__ __mustn't__ contain a header row.

*Boxes data sample*:
```
w 165 480 209 525 0
h 174 478 241 532 0
a 217 512 249 552 0
```

*Output*: 
```json
{
    "char": [
        "w", "h", "a" 
    ],
    "left": [
        165, 174, 217 
    ],
    "bottom": [
        480, 478, 512
    ],
    "right": [
        209, 241, 249
    ],
    "top": [
         525, 532, 552
    ],
    "page": [
        0, 0, 0
    ]
}
```
## tessy.hocr_to_dict(hocr_data)
Converts and return the given __`hocr`__ XML data as a dictionary.

> __`hocr_to_dict` requires the `xmltodict` module to be installed.__    
> The module is __only__ imported if it has already been previously installed.
## tessy.osd_to_dict(osd_data)
Converts and return the given __`osd`__ data as a dictionary.

*OSD data sample*:
```
Page number: 0
Orientation in degrees: 270
Rotate: 90
Orientation confidence: 71.00
Script: Latin
Script confidence: nan
```

*Output*: 
```json
{
    "page_number": 0,
    "orientation_in_degrees": 270,
    "rotate": 90,
    "orientation_confidence": 71.00,
    "script": "Latin",
    "script_confidence": None
}
```

*Note*: Dictionary keys are dynamically generated based on the data content.