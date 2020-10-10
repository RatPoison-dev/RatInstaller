import os, json

DEFAULT_SETTINGS = {
                    "force_install_jdk": False,
                    "force_cheat_update": False,
                    "force_cheat_compile": False,
                    "update_type": "call_installer",
                    "build_folder": "build/",
                    "jdk_zip_name": "JDK.zip",
                    "github_repo": "TheFuckingRat/RatPoison",
                    "settings_directory": "settings/",
                    "bypass_download": False,
                    "show_last_X_commits": 5,
                    "jdk_link": "https://download.java.net/java/GA/jdk14.0.2/205943a0976c4ed48cb16f1043c5c647/12/GPL/openjdk-14.0.2_windows-x64_bin.zip"
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

def loadSettings():
    if (os.path.exists("installerSettings.json")):
        with open("installerSettings.json") as settingsFile:
            return Settings(json.load(settingsFile))
    else:
        return Settings(DEFAULT_SETTINGS)