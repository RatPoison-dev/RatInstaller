import os
import random
import re
import shutil
import stat
import string
import subprocess
import urllib.request
import zipfile
import struct
from pathlib import Path
import requests
from tqdm import tqdm
import settingsTools
import __main__

settings = settingsTools.settings
locales = settingsTools.locales


def get_main():
    return os.path.splitext(os.path.basename(__main__.__file__))[0]

def get_build_state():
    if (folder_name := get_folder_name()) is None: return False
    for _ in Path(folder_name).rglob("*.bat"):
        return True
    return False

def is_running_from_zip():
    tmp_list = [os.path.splitext(os.path.basename(x))[0] for x in os.listdir() if os.path.isfile(x)]
    return os.environ["TEMP"] in os.getcwd() or get_main() not in tmp_list


def get_installed_state():
    return "version.txt" in os.listdir()


def test_internet_connection():
    try:
        requests.get("https://google.com")
        return True
    except Exception:
        return False


def rmtree(path, **kwargs):
    shutil.rmtree(path, onerror=on_rm_error, **kwargs)


def get_folder_name():
    if not os.path.exists(settings["build_folder"]): return None
    for file in Path(settings["build_folder"]).rglob("*.bat"):
        return str(file.parent)
    return None


def get_bat_name():
    if not os.path.exists(settings["build_folder"]): return None
    folder_name = get_folder_name()
    for file in Path(folder_name).rglob("*.bat"):
        return str(file)


def get_settings_path():
    for file in os.listdir(folder_name := get_folder_name()):
        if os.path.exists(os.path.join(file, "CFGS")):
            return os.path.join(folder_name, file)


def get_jar_name():
    if not os.path.exists(settings["build_folder"]): return None
    folder_name = get_folder_name()
    for file in Path(folder_name).rglob("*.jar"):
        return str(file.name)


def start_cheat():
    bat_file = get_bat_name()
    subprocess.run([bat_file])


def migrate_default_settings(folder, save_path):
    cfg = ""
    for file in os.listdir(folder):
        prev_path = os.path.join(folder, file)
        if os.path.isfile(prev_path):
            with open(prev_path, "r") as fr:
                for line in fr:
                    try:
                        splitted = line.split("=")
                        assert len(splitted) >= 2
                        assert "//" not in line
                        cfg += line
                    except AssertionError:
                        pass
    with open(save_path, "w") as fw:
        fw.write(cfg)


def migrate_folder(folder, new_folder):
    for f in os.listdir(folder):
        prev_path = f"{folder}/{f}"
        new_path = f"{new_folder}/{f}"
        if os.path.isfile(prev_path):
            if os.path.exists(new_path):
                os.remove(new_path)
            shutil.move(prev_path, new_path)


class DownloadProgressBar(tqdm):
    def update_to(self, b=1, bsize=1, total_size=None):
        if total_size is not None:
            self.total = total_size
        self.update(b * bsize - self.n)


def extract_file(output_path):
    with zipfile.ZipFile(output_path) as zip_ref:
        zip_ref.extractall("")


def download_file_and_extract(url, output_path, size=None):
    download_file_with_bar(url, output_path, size)
    extract_file(output_path)
    os.remove(output_path)


# https://stackoverflow.com/questions/15644964/python-progress-bar-and-downloads
def download_file_with_bar(url, output_path, size=None):
    with DownloadProgressBar(unit='B', unit_scale=True,
                             miniters=1, desc=url.split('/')[-1], ascii=True) as t:
        urllib.request.urlretrieve(url, filename=output_path, reporthook=lambda b, bsize, tsize: t.update_to(b, bsize,
                                                                                                             size) if size is not None else t.update_to(
            b, bsize, tsize))


# https://stackoverflow.com/questions/4829043/how-to-remove-read-only-attrib-directory-with-python-in-windows
def on_rm_error(func, path, exc_info):
    try:
        subprocess.check_call(f"attrib -H \"{path}\"")
        os.chmod(path, stat.S_IWRITE)
        os.unlink(path)
    except:
        pass


def ask_start_cheat():
    if locales.adv_input("START_CHEAT_INPUT") in locales.yes:
        start_cheat()


def parse_jdk_version(path):
    try:
        return int(re.findall(r"jdk-\d+", path.lower())[0].split("jdk-")[1])
    except Exception:
        return None


def verify_path(path: Path):
    strPath = str(path)
    return path.exists() and "jre" not in strPath.lower() and parse_jdk_version(strPath) is not None and parse_jdk_version(
        strPath) >= 12 and "$RECYCLE.BIN" not in strPath and ((path.is_dir() and os.path.exists(os.path.join(path, "bin"))) or not path.is_dir()) and (
                    "adoptopenjdk" not in strPath.lower() or not is_x64())


def get_random_name():
    s = ""
    for _ in range(20):
        s += random.choice(string.ascii_uppercase)
    return s


def search_file(file):
    path_to_search = os.environ["JAVA_HOME"] if os.environ.get("JAVA_HOME") is not None and verify_path(
        Path(os.environ["JAVA_HOME"])) else os.path.splitdrive(os.getcwd())[0] + "/"
    return Path(path_to_search).rglob(file)


def kill_jdk():
    # kill all processes returned by `jps.exe -q`
    try:
        for path in search_file("jps.exe"):
            str_path = str(path)
            processes = [int(x) for x in subprocess.getoutput(f"\"{str_path}\" -q").split("\n")]
            for process in processes:
                try:
                    os.kill(process, 0)
                except Exception:
                    pass
            break
    except Exception:
        # Nah
        pass

def listdir(path):
    return os.listdir(path) if os.path.exists(path) else []

def mkdirs(path):
    if not os.path.exists(path):
        os.makedirs(path)

def set_java_home(path):
    os.environ["JAVA_HOME"] = os.path.join(os.getcwd(), path)


def is_x64():
    return 'PROCESSOR_ARCHITEW6432' in os.environ or os.environ['PROCESSOR_ARCHITECTURE'].endswith('64')
