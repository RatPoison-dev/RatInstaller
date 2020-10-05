import os, json

class DefaultSettings(object):
    def __init__(self):
        # Define default installer settings here
        self.force_install_jdk = False
        self.force_cheat_update = False
        self.build_folder = "build/"
        self.jdk_link = "https://download.java.net/java/GA/jdk14.0.2/205943a0976c4ed48cb16f1043c5c647/12/GPL/openjdk-14.0.2_windows-x64_bin.zip"
        self.jdk_zip_name = "JDK.zip"
        self.github_repo = "TheFuckingRat/RatPoison"
        self.force_cheat_compile = False
        self.update_type = "call_installer"
        self.bypass_download = False
    def __getitem__(self, key):
        return self.__dict__[key]
    def __str__(self):
        return str(self.__dict__)

def loadSettings():
    if (os.path.exists("installerSettings.json")):
        with open("installerSettings.json") as settingsFile:
            return json.load(settingsFile)
    else:
        return DefaultSettings()