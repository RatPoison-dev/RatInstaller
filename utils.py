import os
import random
import re
import shutil
import stat
import string
import subprocess
import urllib.request
import zipfile
from pathlib import Path

import requests
from tqdm import tqdm

import locales
import settingsTools

settings = settingsTools.loadSettings()
locales = locales.Locales()


def getBuildedState():
    if (folder_name := getFolderName()) == None: return False
    for _ in Path(folder_name).rglob("*.bat"):
        return True
    return False


def getInstalledState():
    # TODO: get file names from all branches and check if none of them are matching with os.listdir()
    return "version.txt" in os.listdir()


def testInternetConnection():
    try:
        requests.get("https://google.com")
        return True
    except:
        return False


def rmtree(path, **kwargs):
    shutil.rmtree(path, onerror=on_rm_error, **kwargs)


def getFolderName():
    if not os.path.exists(settings["build_folder"]): return None
    for file in Path(settings["build_folder"]).rglob("*.bat"):
        return str(file.parent)
    return None


def getBatName():
    if not os.path.exists(settings["build_folder"]): return None
    folder_name = getFolderName()
    for file in Path(folder_name).rglob("*.bat"):
        return str(file)


def getSettingsPath():
    for file in os.listdir(folder_name := getFolderName()):
        if (os.path.exists(os.path.join(file, "CFGS"))):
            return os.path.join(folder_name, file)


def getJarName():
    if not os.path.exists(settings["build_folder"]): return None
    folder_name = getFolderName()
    for file in Path(folder_name).rglob("*.jar"):
        return str(file.name)


def startCheat():
    bat_file = getBatName()
    subprocess.run([bat_file])


def migrateDefaultSettings(folder, savePath):
    cfg = ""
    for file in os.listdir(folder):
        prevpath = os.path.join(folder, file)
        if os.path.isfile(prevpath):
            with open(prevpath, "r") as fr:
                for line in fr:
                    try:
                        splitted = line.split("=")
                        assert len(splitted) >= 2
                        assert not "//" in line
                        cfg += line
                    except AssertionError:
                        pass
    with open(savePath, "w") as fw:
        fw.write(cfg)


def migrateFolder(folder, new_folder):
    for f in os.listdir(folder):
        prev_path = f"{folder}/{f}"
        nwpath = f"{new_folder}/{f}"
        if os.path.isfile(prev_path):
            if os.path.exists(nwpath):
                os.remove(nwpath)
            shutil.move(prev_path, nwpath)


class DownloadProgressBar(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)


def downloadFileAndExtract(url, output_path):
    downloadFileWithBar(url, output_path)
    with zipfile.ZipFile(output_path) as zip_ref:
        zip_ref.extractall("")
    os.remove(output_path)


# https://stackoverflow.com/questions/15644964/python-progress-bar-and-downloads
def downloadFileWithBar(url, output_path):
    with DownloadProgressBar(unit='B', unit_scale=True,
                             miniters=1, desc=url.split('/')[-1], ascii=True) as t:
        urllib.request.urlretrieve(url, filename=output_path, reporthook=t.update_to)


# https://stackoverflow.com/questions/4829043/how-to-remove-read-only-attrib-directory-with-python-in-windows
def on_rm_error(func, path, exc_info):
    try:
        subprocess.check_call(f"attrib -H \"{path}\"")
        os.chmod(path, stat.S_IWRITE)
        os.unlink(path)
    except:
        pass


def askStartCheat():
    if (locales.advInput("START_CHEAT_INPUT") in locales.YES):
        startCheat()


def parseJDKVersion(path):
    try:
        return int(re.findall(r"jdk-\d+", path.lower())[0].split("jdk-")[1])
    except:
        return None


def verifyPath(path):
    return not "jre" in path.lower() and parseJDKVersion(path) is not None and parseJDKVersion(
        path) >= 12 and not "$RECYCLE.BIN" in path


def getRandomName():
    s = ""
    for _ in range(20):
        s += random.choice(string.ascii_uppercase)
    return s


def searchFile(file):
    pathToSearch = os.environ["JAVA_HOME"] if os.environ.get("JAVA_HOME") is not None and verifyPath(
        os.environ["JAVA_HOME"]) else os.path.splitdrive(os.getcwd())[0] + "/"
    return Path(pathToSearch).rglob(file)


def killJDKs():
    # kill all processes returned by `jps.exe -q`
    try:
        for path in searchFile("jps.exe"):
            strPath = str(path)
            processes = [int(x) for x in subprocess.getoutput(f"\"{strPath}\" -q").split("\n")]
            for process in processes:
                try:
                    os.kill(process, 0)
                except:
                    pass
            break
    except:
        # Nah
        pass


def setJavaHome(path):
    os.environ["JAVA_HOME"] = os.path.join(os.getcwd(), path)
