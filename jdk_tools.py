import os
import settingsTools
import utils
import zipfile
import shutil
from pathlib import Path

settings = settingsTools.settings

locales = settingsTools.locales


def jdk_zip_exists():
    zip_name = settings["jdk_zip_name"]
    if os.path.exists(zip_name):
        try:
            with zipfile.ZipFile(zip_name) as zip_ref:
                file_list = [x.filename for x in zip_ref.filelist]
                if "jdk-14.0.2/bin/" in file_list or "jdk-14.0.2+12/bin" in file_list:
                    return True
        except zipfile.BadZipFile:
            os.remove(zip_name)
            return False
    return False

def search_jdk():
    if jdk_zip_exists():
        locales.adv_print(f"JDK_ZIP_ALREADY_EXISTS", variables={"zipfile": settings["jdk_zip_name"]})
        utils.extract_file(settings["jdk_zip_name"])
        os.remove(settings["jdk_zip_name"])
    for file in os.listdir():
        jdk_path = os.path.join(os.getcwd(), file)
        if "jdk" in file and not os.path.isfile(jdk_path) and utils.verify_path(Path(jdk_path)):
            extend_path(jdk_path)
            return True
    p = utils._Path(settings["jdk_installation_path"])
    for file in p.listdir():
        jdk_path = os.path.join(p.value, file)
        if "jdk" in file and os.path.isdir(jdk_path) and utils.verify_path(Path(jdk_path)):
            extend_path(os.path.join(p.value, file))
            utils.set_java_home(os.path.join(p.value, file))
            return True
    jdk = os.environ.get("JAVA_HOME")
    return settings["skip_jdk_checks"] or (jdk is not None and utils.verify_path(Path(jdk)))

def extend_path(pov):
    utils.set_java_home(pov)
    os.environ["PATH"] = os.environ["PATH"] + ";" + os.path.join(os.environ["JAVA_HOME"], "bin")



def download_jdk():
    if not search_jdk() or settings["force_install_jdk"]:
        jdk_link = settings["jdk_link_x64"] if utils.is_x64() else settings["jdk_link_x86"]
        jdk_zip_name = settings["jdk_zip_name"]
        extracted = utils.download_file_and_extract(jdk_link, jdk_zip_name)
        if not extracted:
            print("Extracting JDK have failed. Redownloading...")
            download_jdk()
        else:
            pass
        os.rename("jdk-14.0.2+12", "jdk-14.0.2") if os.path.exists("jdk-14.0.2+12") else None
        default_directory = os.environ.get("APPDATA") if os.environ.get("APPDATA") is not None else os.getcwd()
        created = utils.mkdirs(default_directory)
        if not created:
            directory = os.getcwd() # failed to create directory, can't do much here
        else:
            directory = default_directory
        new_directory = os.path.join(directory, "jdk-14.0.2")
        if os.path.exists(new_directory): shutil.rmtree(new_directory)
        try:
            shutil.move("jdk-14.0.2", directory)
        except:
            directory = os.getcwd()
        # Set JAVA_HOME and PATH
        extend_path(os.path.join(directory, "jdk-14.0.2"))
        settings.setKey("jdk_installation_path", directory, False)
