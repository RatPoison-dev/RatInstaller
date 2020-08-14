import os, json

class DefaultSettings(object):
    def __init__(self):
        # Define default installer settings here
        self.force_install_jdk = False
    def __getitem__(self, key):
        return self.__dict__[key]

def loadSettings():
    if (os.path.exists("settings.json")):
        with open("settings.json") as settingsFile:
            return json.loads(settingsFile)
    else:
        return DefaultSettings()