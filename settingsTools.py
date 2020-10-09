import os, json

DEFAULT_SETTINGS = {'build_folder': 'build/',
                    'bypass_download': False,
                    'force_cheat_compile': False, 
                    'force_cheat_update': False, 
                    'force_install_jdk': False, 
                    'github_repo': 'TheFuckingRat/RatPoison', 
                    'jdk_link': 'https://download.jav...64_bin.zip', 
                    'jdk_zip_name': 'JDK.zip', 
                    'update_type': 'call_installer'
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