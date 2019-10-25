import glob
import importlib
import ntpath
import os
import platform
import shlex
import shutil
import string
import subprocess
import sys
import tempfile
import warnings

try:
    import winreg
except ImportError:
    pass

from distutils.version import LooseVersion
from enum import Enum
from pathlib import Path

XMLTODICT_INSTALLED = importlib.util.find_spec("xmltodict") is not None

if XMLTODICT_INSTALLED:
    import json
    import xmltodict


# -------------------------------------------------------------------
# TessyLang
# -------------------------------------------------------------------
class TessyLang(Enum):

    AFRIKAANS = "afr"
    AMHARIC = "amh"
    ARABIC = "ara"
    ASSAMESE = "asm"
    AZERBAIJANI = "aze"
    AZERBAIJANI_CYRILLIC = "aze_cyrl"
    BELARUSIAN = "bel"
    BENGALI = "ben"
    TIBETAN = "bod"
    BOSNIAN = "bos"
    BULGARIAN = "bul"
    CATALAN_VALENCIAN = "cat"
    CEBUANO = "ceb"
    CZECH = "ces"
    CHINESE_SIMPLIFIED = "chi_sim"
    CHINESE_TRADITIONAL = "chi_tra"
    CHEROKEE = "chr"
    WELSH = "cym"
    DANISH = "dan"
    GERMAN = "deu"
    DZONGKHA = "dzo"
    GREEK_MODERN = "ell"
    ENGLISH = "eng"
    ENGLISH_MIDDLE = "enm"
    ESPERANTO = "epo"
    ESTONIAN = "est"
    BASQUE = "eus"
    PERSIAN = "fas"
    FINNISH = "fin"
    FRENCH = "fra"
    FRANKISH = "frk"
    FRENCH_MIDDLE = "frm"
    IRISH = "gle"
    GALICIAN = "glg"
    GREEK_ANCIENT = "grc"
    GUJARATI = "guj"
    HAITIAN = "hat"
    HAITIAN_CREOLE = "hat"
    HEBREW = "heb"
    HINDI = "hin"
    CROATIAN = "hrv"
    HUNGARIAN = "hun"
    INUKTITUT = "iku"
    INDONESIAN = "ind"
    ICELANDIC = "isl"
    ITALIAN = "ita"
    ITALIAN_OLD = "ita_old"
    JAVANESE = "jav"
    JAPANESE = "jpn"
    KANNADA = "kan"
    GEORGIAN = "kat"
    GEORGIAN_OLD = "kat_old"
    KAZAKH = "kaz"
    CENTRAL_KHMER = "khm"
    KIRGHIZ = "kir"
    KYRGYZ = "kir"
    KOREAN = "kor"
    KURDISH = "kur"
    LAO = "lao"
    LATIN = "lat"
    LATVIAN = "lav"
    LITHUANIAN = "lit"
    MALAYALAM = "mal"
    MARATHI = "mar"
    MACEDONIAN = "mkd"
    MALTESE = "mlt"
    MALAY = "msa"
    BURMESE = "mya"
    NEPALI = "nep"
    DUTCH = "nld"
    FLEMISH = "nld"
    NORWEGIAN = "nor"
    ORIYA = "ori"
    PANJABI = "pan"
    PUNJABI = "pan"
    POLISH = "pol"
    PORTUGUESE = "por"
    PUSHTO = "pus"
    PASHTO = "pus"
    ROMANIAN = "ron"
    MOLDAVIAN = "ron"
    MOLDOVAN = "ron"
    RUSSIAN = "rus"
    SANSKRIT = "san"
    SINHALA = "sin"
    SINHALESE = "sin"
    SLOVAK = "slk"
    SLOVENIAN = "slv"
    SPANISH = "spa"
    CASTILIAN = "spa"
    SPANISH_OLD = "spa_old"
    CASTILIAN_OLD = "spa_old"
    ALBANIAN = "sqi"
    SERBIAN = "srp"
    SERBIAN_LATIN = "srp_latn"
    SWAHILI = "swa"
    SWEDISH = "swe"
    SYRIAC = "syr"
    TAMIL = "tam"
    TELUGU = "tel"
    TAJIK = "tgk"
    TAGALOG = "tgl"
    THAI = "tha"
    TIGRINYA = "tir"
    TURKISH = "tur"
    UIGHUR = "uig"
    UYGHUR = "uig"
    UKRAINIAN = "ukr"
    URDU = "urd"
    UZBEK = "uzb"
    UZBEK_CYRILLIC = "uzb_cyrl"
    VIETNAMESE = "vie"
    YIDDISH = "yid"

    @classmethod
    def contains(cls, value):
        return any(value == item.value for item in cls)

    @classmethod
    def join(cls, *args):
        result = []

        if len(args) > 0:
            if isinstance(args[0], (list, tuple)):
                return TessyLang.join(*args[0])

            langs = []

            for lang in args:
                if isinstance(lang, TessyLang):
                    lang = lang.value
                elif isinstance(lang, str):
                    lang = lang.strip()
                else:
                    raise ValueError(
                        "join: Only string and TessyLang types are supported. "
                        "Given type: {0}".format(str(type(lang)))
                    )
                    continue

                if not TessyLang.contains(lang):
                    raise ValueError(
                        "join: The given language '{0}' doesn't exists "
                        "or not supported yet.".format(lang)
                    )
                    continue

                langs.append(lang)

            if langs:
                result = "+".join(langs)

        return result

    def __str__(self):
        return str(self.value)


# -------------------------------------------------------------------
# TessyWarning
# -------------------------------------------------------------------
TessyWarning = type("TessyWarning", (Warning,), {})


# -------------------------------------------------------------------
# Tessy
# -------------------------------------------------------------------
Lang = TessyLang

DataOutput = type(
    "TessyDataOutput", (object,), {"BYTES": "bytes", "STRING": "str", "DICT": "dict"}
)

_config = type(
    "TessyConfig",
    (object,),
    {
        # Tesseract command <or> binary path (absolute)
        "command": "tesseract",
        # Tesseract date directory path (absolute)
        "datadir": None,
        # Content separator used when multiple files content are merged
        # into a single string
        "contentsep": "||||",
        # Cache file who may contains the Tesseract binary path (absolute)
        "pathfile": ".TESSPATH",
        # Windows Tesseract registry key path (HKEY_LOCAL_MACHINE)
        "winregkey": "SOFTWARE\Tesseract-OCR",
    },
)

# List of temporary files created by the module
_tempfiles = []

# Supported image modules holder
_image_modules = {"pil": None, "wx": None, "qt": None, "cv": None}

# Equals true if the system's OS is a Windows-based OS
_platform_windows = platform.system().lower() == "windows"


def command():
    return _config.command


def set_command(cmd, check_runnable=False, write_cache=False):
    if cmd:
        _config.command = cmd.strip()

        if check_runnable and not runnable():
            _warn("set_command: The given command ({0}) is not runnable".format(cmd))

        if write_cache:
            _write_file(
                os.path.join(_get_temp_dir(), _config.pathfile), _config.command
            )
    else:
        _warn("set_command: Invalid command: {0}".format(cmd))


def data_dir():
    return _config.datadir


def set_data_dir(datadir, update_env=True):
    if os.path.isdir(datadir):
        _config.datadir = datadir

        if update_env:
            os.environ["TESSDATA_PREFIX"] = _config.datadir
    else:
        _warn("set_data_dir: Invalid directory: '{0}'".format(datadir))


def content_sep():
    return _config.contentsep


def set_content_sep(sep):
    if sep:
        _config.contentsep = sep
    else:
        _warn("set_content_sep: Invalid separator: {0}".format(sep))


def configure(**kw):
    result = True
    invalid_args = []

    if kw:
        for k, v in kw.items():
            if "command" in k:
                set_command(v)
            elif "data_dir" in k:
                set_data_dir(v)
            elif "content_sep" in k:
                set_content_sep(v)
            else:
                invalid_args.append(k)
    else:
        invalid_args.append("<unspecified>")

    if invalid_args:
        result = False
        _warn("configure: Invalid argument(s): {0}".format(", ".join(invalid_args)))

    return result


def init():
    if not runnable():
        tess_loc = locate()

        if tess_loc:
            set_command(tess_loc, True)

    tess_data_loc = locate_data()

    if tess_data_loc:
        set_data_dir(tess_data_loc)


def image_to_file(
    image, output_filename_base=None, output_format="txt", lang=None, config=None
):
    result = []

    # Checks if the Tesseract data directory has been specified somewhere
    data_arg_given = config and "--tessdata-dir" in config

    if (
        not _config.datadir
        and not data_arg_given
        and not "TESSDATA_PREFIX" in os.environ
    ):
        _warn(
            ""
            "image_to_file: The Tesseract data directory path hasn't been specified, "
            "the command may fail.\n"
            "You can specify the location of tessdata path by:\n"
            " - Calling the 'set_data_dir(<PATH>)' function of this module,\n"
            " - Adding the '--tessdata-dir <PATH>' parameter using the 'config' "
            "variable when calling any 'image_to' function,\n"
            " - Adding the 'TESSDATA_PREFIX' environment variable in your OS."
            ""
        )

    # Creates a temporary file name for both input and output files
    in_file = os.path.join(_get_temp_dir(), _get_temp_file_name())
    out_file = (
        os.path.join(_get_temp_dir(), _get_temp_file_name())
        if output_filename_base is None
        else output_filename_base
    )

    # 'output_format' can be a string, a list or a tuple
    if isinstance(output_format, str):
        # Remove all whitespace
        output_format = output_format.lower().replace(" ", "")

        # Converts as a tuple (it may contains multiple formats)
        if "," in output_format:
            output_format = tuple(output_format.split(","))
        else:
            output_format = (output_format,)
    elif isinstance(output_format, (tuple, list)):
        # All format must be in lowercase
        output_format = tuple(fmt.strip().lower() for fmt in output_format)
    else:
        # The given format is undefined/unsupported
        _warn(
            "image_to_file: Unsupported output format. 'output_format' "
            "must be a string, a list or a tuple."
        )
        return result

    # If 'image' is a string (who should contains the input file path),
    # just copy the image file at the input temp file location
    if isinstance(image, str):
        try:
            shutil.copyfile(image, in_file)
        except IOError as e:
            _warn(
                "image_to_file: Unable to copy the file '{0}' to '{1}'.\n"
                "I/O Error ({2}): {3}.".format(image, in_file, e.errno, e.strerror)
            )

    # We must determine which library must to be imported to work
    # with the given 'image' object
    # Supported libs: PIL/Pillow, wxPython, PyQt 4/5, PySide and OpenCV
    else:
        # Gets both library acronym and plain name.
        # - The acronym is used internally as identifier
        # - The plain name is used for debugging
        img_lib_name, img_lib_plain_name = _get_image_lib_name_from_object(image)

        if not img_lib_name:
            _warn(
                "image_to_file: Unsupported image. 'image' must be an PIL "
                "Image, wxPython Image, PyQt/PySide QImage or OpenCV Image (ndarray)."
            )
            return result

        # Try to import the corresponding image module
        img_mod = _import_image_module(img_lib_name)

        if not img_mod:
            _warn(
                "image_to_file: Import Error: Unable to import the "
                "image module from the lib {0}.".format(img_lib_plain_name)
            )
            return result

        # Prepare the image using the imported module
        _prepare_image(image, img_lib_name, img_mod, in_file)

    # If the image has been prepared successfully, the file should be present
    if os.path.isfile(in_file):
        global _tempfiles

        _tempfiles.append(in_file)

        # Gets the command
        tess_cmd = _config.command

        # Make a unaltered copy of the output filename
        out_file_clean = out_file

        if " " in tess_cmd:
            tess_cmd = _escape_path(tess_cmd)

        if " " in in_file or " " in out_file:
            in_file = _escape_path(in_file)
            out_file = _escape_path(out_file)

        # Build the standard command
        command = [tess_cmd, in_file, out_file]

        # Add any extra user-defined parameters
        if config:
            try:
                command += shlex.split(config)
            except Exception as e:
                _warn(
                    "image_to_file: Unable to parse the 'config' content. "
                    "Extra parameter(s) will be ignored.\nError: {0}.".format(e)
                )

        if "osd" in output_format and not "--psm" in command:
            command += ["--psm", "0"]

        # Adds the given language(s)
        # 'lang' can be a string, a tuple/list of string,
        # a TessyLang instance or a tuple/list of TessyLang instances
        if lang:
            if isinstance(lang, TessyLang):
                lang = TessyLang.join(lang)
            elif isinstance(lang, (list, tuple)):
                lang = TessyLang.join(*lang)

            command += ["-l", lang]

        # .txt format support (default)
        if "txt" in output_format:
            command += ["txt"]

        # .box format support
        if "box" in output_format:
            command += ["batch.nochop", "makebox"]

        # .pdf format support
        if "pdf" in output_format:
            command += ["pdf"]

        # .hocr format support
        if "hocr" in output_format:
            command += ["hocr"]

        # .tsv format support
        if "tsv" in output_format:
            command += ["tsv"]

        # Converts the command as string
        command_str = " ".join(command)

        # Run the command
        status, output, err_string = _proc_exec_wait(command_str)

        # The command has been executed successfully
        if status == 0:
            output_files = list(
                filter(
                    lambda file: os.path.isfile(file),
                    list(
                        map(
                            lambda fmt: "{0}.{1}".format(out_file_clean, fmt),
                            output_format,
                        )
                    ),
                )
            )

            if output_files:
                _tempfiles.extend(output_files)
                result.extend(output_files)
        # Tesseract raised error(s)
        else:
            errors = _parse_errors(err_string)

            if errors:
                _warn(
                    "image_to_file: Error while executing Tesseract, "
                    "returned error(s):\n{0}.".format(errors)
                )

    return result


def image_to_data(
    image, output_format="txt", data_output=DataOutput.STRING, lang=None, config=None
):
    result = None

    # PDF format is not supported by this function
    if output_format and "pdf" in output_format:
        _warn(
            "image_to_data: PDF format is not supported by this function, "
            "use 'image_to_file' instead."
        )
        return result

    # Call 'image_to_file' function to get the output file(s) list
    out_files = image_to_file(image, None, output_format, lang, config)

    if out_files and len(out_files) > 0:
        result = []

        todict_func = {
            "txt": lambda d: {"data": d},
            "tsv": lambda d: sv_to_dict(d),
            "box": lambda d: boxes_to_dict(d),
            "hocr": lambda d: hocr_to_dict(d),
            "osd": lambda d: osd_to_dict(d),
        }

        for fp in out_files:
            file_data = _read_file(fp, data_output == DataOutput.BYTES)
            file_ext = os.path.splitext(fp)[1][1:]

            if file_data:
                if data_output == DataOutput.DICT:
                    file_data = todict_func[file_ext](file_data)

                result.append(file_data)

        clear_temp(False)

    return result


def image_to_string(image, output_format="txt", lang=None, config=None):
    result = None

    # PDF format is not supported by this function
    if output_format and "pdf" in output_format:
        _warn(
            "image_to_string: PDF format is not supported by this function, "
            "use 'image_to_file' instead."
        )
        return result

    # Call 'image_to_data' function to get the output data list
    out_datas = image_to_data(image, output_format, DataOutput.STRING, lang, config)

    if out_datas:
        result = _config.contentsep.join(out_datas)
        clear_temp(False)

    return result


def locate():
    result = None

    # Locate sub functions: fastest to slowest
    loc_func = {
        # key, Windows only?, function
        "cache": (False, _locate_from_cache_file),
        "registry": (True, _locate_from_registry)
    }

    for key, value in loc_func.items():
        win_only, func = value

        if win_only and not _platform_windows:
            continue

        loc = func()

        if loc and os.path.isfile(loc):
            result = loc
            break

    return result


def locate_data():
    # Locate by using the environment variable
    if "TESSDATA_PREFIX" in os.environ:
        data_prefix = os.environ["TESSDATA_PREFIX"]

        if os.path.isdir(data_prefix):
            return data_prefix

    # Locate by using the command directory
    cmd_path = os.path.dirname(_config.command)

    if cmd_path:
        cmd_data_path = os.path.join(cmd_path, "tessdata")

        if os.path.isdir(cmd_data_path):
            return cmd_data_path

    return None


def run(command=None, silent=False):
    command = command if command else _config.command
    return _proc_exec_wait(command, silent)


start = run


def runnable():
    return tesseract_version() is not None


def tesseract_version():
    result = None

    try:
        command = _config.command

        if " " in command:
            command = _escape_path(command)

        command += " --version"
        status, output, err_string = _proc_exec_wait(command, True)

        if status == 0:
            result = LooseVersion(output.split()[1].lstrip(string.printable[10:]))
    except Exception as e:
        _warn(
            "tesseract_version: Unable to retrieve Tesseract "
            "version. Error: {0}".format(e)
        )

    return result


def clear_cache():
    """ Tries to remove the .TESSPATH file."""
    path_file = os.path.join(_get_temp_dir(), _config.pathfile)
    return _remove_file(path_file) if os.path.isfile(path_file) else False


def clear_temp(remove_all=True):
    tf_list = []

    if remove_all:
        temp_dir = _get_temp_dir()
        temp_dir += (
            os.path.sep if os.path.sep not in temp_dir[len(temp_dir) - 1] else ""
        )
        tf_list = glob.glob("{0}TESS_*".format(temp_dir))
    else:
        global _tempfiles

        tf_list = list(_tempfiles)
        _tempfiles.clear()

    for tf in tf_list:
        if os.path.isfile(tf):
            _remove_file(tf)


def sv_to_dict(sv_data, cell_delimiter="\t"):
    result = {}
    rows = [row.split(cell_delimiter) for row in sv_data.splitlines()]

    if rows:
        header = rows.pop(0)
        header_len = len(header)

        for idx, header_col in enumerate(header):
            result[header_col] = []

            for row in rows:
                # Makes sure all rows size equals header's size
                if len(row) < header_len:
                    [row.append("") for x in range(0, (header_len - len(row)))]

                row_val = int(row[idx]) if row[idx].isdigit() else row[idx]
                result[header_col].append(row_val)

    return result


def boxes_to_dict(boxes_data):
    boxes_data = "{0}\n{1}".format("char left bottom right top page", boxes_data)

    return sv_to_dict(boxes_data, " ")


def hocr_to_dict(hocr_data):
    result = {}

    if not XMLTODICT_INSTALLED:
        _warn(
            "hocr_to_dict: Unable to parse hocr data: The 'xmltodict' module is missing."
            "Ensure to install it using `pip install -U xmltodict` before calling "
            "this function"
        )
    else:
        try:
            result = json.dumps(xmltodict.parse(hocr_data), indent=4)
        except (Exception, ValueError) as e:
            _warn("hocr_to_dict: Unable to parse hocr data: {0}.".format(e))

    return result


def osd_to_dict(osd_data):
    result = {}

    def _conv_prop_value(s):
        cresult = s
        if s.isdigit() or "." in s:
            try:
                cresult = float(s) if "." in s else int(s)
            except ValueError:
                pass
        elif "nan" in s.lower():
            cresult = None
        return cresult

    data = [line.strip().split(": ") for line in osd_data.splitlines()]

    for prop in data:
        prop_key = prop[0].lower().strip().replace(" ", "_")
        prop_value = _conv_prop_value(prop[1])
        result[prop_key] = prop_value

    return result


def _locate_from_cache_file():
    path_file = os.path.join(_get_temp_dir(), _config.pathfile)
    return _read_file(path_file) if os.path.isfile(path_file) else None


def _locate_from_registry():
    result = None

    try:
        registry = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)

        with winreg.OpenKey(registry, _config.winregkey) as key:
            key_val = winreg.QueryValueEx(key, "Path")
            result = "{0}\\tesseract.exe".format(key_val[0])
    except OSError as e:
        _warn(
            "_locate_from_registry: Could not open the registry key: "
            "'{0}'. Error: {1}".format(_config.winregkey, e)
        )

    return result


def _get_image_lib_name_from_object(obj):
    # Hackish way to determine from which image lib 'obj' come from
    # without importing each lib module individually.
    result = ()

    if obj is not None:
        # PIL/Pillow Image
        if hasattr(obj, "_close_exclusive_fp_after_loading"):
            result = ("pil", "PIL/Pillow")
        # wxPython Image
        elif hasattr(obj, "FindFirstUnusedColour") and hasattr(
            obj, "GetImageExtWildcard"
        ):
            result = ("wx", "wxPython")
        # PyQt4, PyQt5 or PySide QImage
        elif hasattr(obj, "createHeuristicMask") and hasattr(obj, "setDotsPerMeterX"):
            result = ("qt", "PyQt(4-5)/PySide(1.x)")
        # OpenCV Image (NumPy ndarray)
        elif hasattr(obj, "argpartition") and hasattr(obj, "newbyteorder"):
            result = ("cv", "OpenCV")

    return result


def _import_image_module(mn):
    global _image_modules

    result = None

    # Don't re-import existing cached modules
    if mn in _image_modules and _image_modules[mn] is not None:
        result = _image_modules[mn]
    else:
        # Import the 'Image' module from PIL
        if mn == "pil":
            try:
                result = importlib.import_module("PIL.Image")
            except (ImportError, RuntimeError):
                pass

        # Import wxPython
        elif mn == "wx":
            try:
                result = importlib.import_module("wx")
            except (ImportError, RuntimeError):
                pass

        # Import the 'QImage' module from PyQt5, PyQt4 or PySide
        elif mn == "qt":
            try:
                result = importlib.import_module("PyQt5.QtGui.QImage")
            except (ImportError, RuntimeError):
                try:
                    result = importlib.import_module("PyQt4.QtGui.QImage")
                except (ImportError, RuntimeError):
                    try:
                        result = importlib.import_module("PySide.QtGui.QImage")
                    except ImportError:
                        pass

        # Import OpenCV
        elif mn == "cv":
            try:
                result = importlib.import_module("cv2")
            except (ImportError, RuntimeError):
                pass

        if result:
            _image_modules[mn] = result

    return result


def _prepare_image(image, img_lib_name, img_mod, img_save_path):
    # The procedure is the same for each lib:
    # - Make a clone of the given image to avoid modifications of the original object
    # - Remove/clear the alpha channel (if exists)
    # - Save the cloned image at the given save path location
    # - Delete the cloned image object

    # PIL/Pillow
    if img_lib_name == "pil":
        pil_image = image.copy()

        try:
            chan = pil_image.split()

            if len(chan) == 4:
                pil_image = img_mod.merge("RGB", (chan[0], chan[1], chan[2]))

            try:
                pil_image.save(img_save_path, "BMP")
            except IOError as e:
                _warn(
                    "_prepare_image: (PIL/Pillow) Could not save the image to '{0}'. "
                    "I/O Error ({1}): {2}.".format(img_save_path, e.errno, e.strerror)
                )
        except Exception as e:
            _warn(
                "_prepare_image: (PIL/Pillow) Unable to split and convert "
                "the image to RGB. Error: {0}.".format(e)
            )
        finally:
            del pil_image

    # wxPython
    elif img_lib_name == "wx":
        wx_image = image.Copy()

        try:
            # No idea if 'ClearAlpha' can raise an exception or not
            if wx_image.HasAlpha():
                wx_image.ClearAlpha()

            try:
                wx_image.SaveFile(img_save_path, img_mod.BITMAP_TYPE_BMP)
            except IOError as e:
                _warn(
                    "_prepare_image: (wxPython) Could not save the image to '{0}'. "
                    "I/O Error({1}): {2}.".format(img_save_path, e.errno, e.strerror)
                )
        except Exception as e:
            _warn(
                "_prepare_image: (wxPython) Unable to remove the alpha channel "
                "from the image. Error: {0}.".format(e)
            )
        finally:
            del wx_image

    # PyQt/PySide
    elif img_lib_name == "qt":
        qt_image = img_mod(image)

        try:
            if qt_image.hasAlphaChannel():
                qt_image = qt_image.convertToFormat(img_mod.Format_RGB32)

            try:
                # Save the image with max quality
                qt_image.save(img_save_path, "BMP", 100)
            except Exception as e:
                _warn(
                    "_prepare_image: (PyQt/PySide) Could not save the image to "
                    "'{0}'. Error: {1}.".format(img_save_path, e)
                )
        except Exception as e:
            _warn(
                "_prepare_image: (PyQt/PySide) Unable to convert the image to RGB."
                "Error: {0}.".format(e)
            )
        finally:
            del qt_image

    # OpenCV
    elif img_lib_name == "cv":
        cv_image = image.copy()

        # OpenCV 'imwrite' require a valid file extension
        img_save_path_bmp = "{0}.bmp".format(img_save_path)

        try:
            if len(cv_image.shape) > 2 and cv_image.shape[2] == 4:
                cv_image = cv_image[:, :, :3]

            if img_mod.imwrite(img_save_path_bmp, cv_image):
                try:
                    os.rename(img_save_path_bmp, img_save_path)
                except OSError as e:
                    _warn(
                        "_prepare_image: (OpenCV) Could not rename the image "
                        "file from '{0}' to '{1}'. Error: {2}.".format(
                            img_save_path_bmp, img_save_path, e
                        )
                    )
            else:
                _warn(
                    "_prepare_image: (OpenCV) Could not save the image to "
                    "'{0}'.".format(img_save_path_bmp)
                )
        except Exception as e:
            _warn(
                "_prepare_image: (OpenCV) Unable to remove the alpha channel "
                "from the image. Error: {0}.".format(e)
            )
        finally:
            del cv_image


def _proc_exec_wait(command_line, silent=False):
    result = (None, None, None)
    command = None
    proc = None

    try:
        if _platform_windows:
            command = command_line.replace("\\", "/")

        command = shlex.split(command)
    except Exception as e:
        _warn(
            "_proc_exec_wait: Unable to parse the given command line: {0}\n"
            "Error: {1}.".format(command_line, e)
        )
        return result

    try:
        sp_kwargs = {
            "stdout": subprocess.PIPE,
            "stderr": subprocess.PIPE,
            "startupinfo": None,
            "env": os.environ,
        }

        if _platform_windows:
            sp_kwargs["startupinfo"] = subprocess.STARTUPINFO()
            sp_kwargs["startupinfo"].dwFlags = (
                subprocess.CREATE_NEW_CONSOLE | subprocess.STARTF_USESHOWWINDOW
            )
            sp_kwargs["startupinfo"].wShowWindow = subprocess.SW_HIDE

        proc = subprocess.Popen(command, **sp_kwargs)
        stdoutdata, stderrdata = proc.communicate()
        status = proc.returncode
        result = (status, stdoutdata.decode("utf8"), stderrdata.decode("utf8"))
    except Exception as e:
        if not silent:
            _warn(
                "_proc_exec_wait: Could not open the process: '{0}'\n"
                "Error: {1}.".format(command[0], e)
            )
    finally:
        if proc:
            if proc.stdout:
                proc.stdout.close()

            if proc.stderr:
                proc.stderr.close()

    return result


def _get_temp_dir():
    result = tempfile.gettempdir()

    if not _platform_windows:
        preserved_tempdir = "/var/tmp"

        if os.path.isdir(preserved_tempdir):
            result = preserved_tempdir

    return result


def _get_temp_file_name():
    tmpfile = tempfile.NamedTemporaryFile(prefix="TESS_")
    h, t = ntpath.split(tmpfile.name)
    return t or ntpath.basename(h)


def _read_file(filepath, return_bytes=False):
    result = None

    try:
        with open(filepath, "rb") as f:
            result = f.read() if return_bytes else f.read().decode("utf-8").strip()
    except IOError as e:
        _warn(
            "_read_file: Could not read the file '{0}'\n"
            "I/O Error ({1}): {2}.".format(filepath, e.errno, e.strerror)
        )
    except UnicodeError as ue:
        _warn(
            "_read_file: Could not read the file '{0}'\n"
            "Unicode Error: {1}.".format(filepath, ue)
        )

    return result


def _remove_file(filepath):
    result = True

    try:
        os.remove(filepath)
    except OSError as e:
        result = False
        _warn(
            "_remove_file: Could not delete the file: '{0}'.\n"
            "OS Error ({1}): {2}.".format(filepath, e.errno, e.strerror)
        )


def _write_file(filepath, content):
    result = True

    try:
        with open(filepath, "w") as f:
            f.write(content)
    except IOError as e:
        result = False
        _warn(
            "_write_file: Could not write the file '{0}'\n"
            "I/O Error ({1}): {2}.".format(filepath, e.errno, e.strerror)
        )

    return result


def _escape_path(path):
    # - On Windows encloses the path if it contains space(s)
    # - On Linux/MacOS prefix any space with a backslash
    path = path.strip()
    return '"{0}"'.format(path) if _platform_windows else path.replace(" ", "\ ")


def _parse_errors(error_string):
    result = error_string

    if error_string:
        lines = error_string.splitlines()
        error_lines = tuple(line for line in lines if line.find("Error") >= 0)

        if len(error_lines) > 0:
            result = "\n".join(error_lines)
        else:
            result = error_string.strip()

    return result


def _warn(msg):
    warnings.warn(msg, TessyWarning, stacklevel=3)
