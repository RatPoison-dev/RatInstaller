import locales
import os
import settingsTools
import utils

settings = settingsTools.load_settings()

locales = locales.Locales()


def search_jdk():
    for file in os.listdir():
        if "jdk" in file and not os.path.isfile(os.path.join(".", file)):
            utils.set_java_home(file)
            return True
    jdk = os.environ.get("JAVA_HOME")
    # why tf your jdk points to recycle bin bitch are you retarted
    return jdk is not None and utils.verify_path(jdk)


def download_jdk():
    if not search_jdk() or settings["force_install_jdk"]:
        jdk_link = settings["jdk_link_x64"] if utils.is_x64() else settings["jdk_link_x86"]
        jdk_zip_name = settings["jdk_zip_name"]
        utils.download_file_and_extract(jdk_link, jdk_zip_name)
        os.rename("jdk-14.0.2+12", "jdk-14.0.2") if os.path.exists("jdk-14.0.2+12") else None
        # Set JAVA_HOME and PATH
        utils.set_java_home("jdk-14.0.2")
        os.environ["PATH"] = os.environ["PATH"] + ";" + os.path.join(os.environ["JAVA_HOME"], "bin")
