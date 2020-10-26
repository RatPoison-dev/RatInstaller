import os
import settingsTools
import utils
import zipfile
from pathlib import Path

settings = settingsTools.settings

locales = settingsTools.locales


def jdk_zip_exists():
    if os.path.exists(settings["jdk_zip_name"]):
        with zipfile.ZipFile(settings["jdk_zip_name"]) as zip_ref:
            file_list = [x.filename for x in zip_ref.filelist]
            if "jdk-14.0.2/bin/" in file_list or "jdk-14.0.2+12/bin" in file_list:
                return True
    return False

def search_jdk():
    for file in os.listdir():
        if "jdk" in file and not os.path.isfile(os.path.join(".", file)):
            utils.set_java_home(file)
            return True
    jdk = os.environ.get("JAVA_HOME")
    # why tf your jdk points to recycle bin bitch are you retarted
    return settings["skip_jdk_checks"] or (jdk is not None and utils.verify_path(Path(jdk)))

def extend_path():
    utils.set_java_home("jdk-14.0.2")
    os.environ["PATH"] = os.environ["PATH"] + ";" + os.path.join(os.environ["JAVA_HOME"], "bin")



def download_jdk():
    if not search_jdk() or settings["force_install_jdk"]:
        jdk_link = settings["jdk_link_x64"] if utils.is_x64() else settings["jdk_link_x86"]
        jdk_zip_name = settings["jdk_zip_name"]
        utils.download_file_and_extract(jdk_link, jdk_zip_name)
        os.rename("jdk-14.0.2+12", "jdk-14.0.2") if os.path.exists("jdk-14.0.2+12") else None
        # Set JAVA_HOME and PATH
        extend_path()
