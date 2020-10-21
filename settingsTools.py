import json
import os

DEFAULT_SETTINGS = {
    "force_install_jdk": false,
    "force_cheat_update": false,
    "force_cheat_compile": false,
    "download_missing_files": true,
    "update_type": "call_installer",
    "build_folder": "build/",
    "jdk_zip_name": "JDK.zip",
    "github_repo": "TheRatCode/RatPoison",
    "settings_directory": "settings/",
    "bypass_download": false,
    "show_last_X_commits": 5,
    "jdk_link_x64": "https://download.java.net/java/GA/jdk14.0.2/205943a0976c4ed48cb16f1043c5c647/12/GPL/openjdk-14.0"
                    ".2_windows-x64_bin.zip",
    "jdk_link_x84": "https://github.com/AdoptOpenJDK/openjdk14-binaries/releases/download/jdk-14.0.2%2B12/OpenJDK14U"
                    "-jdk_x86-32_windows_hotspot_14.0.2_12.zip "
}


class Settings(object):
    def __init__(self, dict):
        self.dict = dict

    def __getitem__(self, key):
        return self.dict[key]

    def __str__(self):
        return str(self.__dict__)

    @property
    def repository_name(self):
        return self.dict.get("github_repo").split("/")[1]


def load_settings():
    if os.path.exists("installerSettings.json"):
        with open("installerSettings.json") as settingsFile:
            return Settings(json.load(settingsFile))
    else:
        return Settings(DEFAULT_SETTINGS)
