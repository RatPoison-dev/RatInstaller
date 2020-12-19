import requests
import json
import os
import typing
import locale
import urllib

DEFAULT_SETTINGS = {
    "force_install_jdk": False,
    "force_cheat_update": False,
    "force_cheat_compile": False,
    "download_missing_files": False,
    "update_type": "call_installer",
    "build_folder": "build/",
    "jdk_zip_name": "JDK.zip",
    "github_repo": "TheRatCode/RatPoison",
    "settings_directory": "settings/",
    "bypass_download": False,
    "skip_jdk_checks": False,
    "show_last_X_commits": 5,
    "jdk_link_x64": "https://download.java.net/java/GA/jdk14.0.2/205943a0976c4ed48cb16f1043c5c647/12/GPL/openjdk-14.0"
                    ".2_windows-x64_bin.zip",
    "jdk_link_x86": "https://github.com/AdoptOpenJDK/openjdk14-binaries/releases/download/jdk-14.0.2%2B12/OpenJDK14U"
                    "-jdk_x86-32_windows_hotspot_14.0.2_12.zip "
}

DEFAULT_LOCALES = {
    "YES": ["y", "yes"],
    "YES_OR_NO": "[Y/N]",
    "JDK_ZIP_ALREADY_EXISTS": "!zipfile already exists. Extracting.",
    "RETRY_BUILD_INPUT": "Build failed. Would you like to have installer download JDK for you and try again?",
    "KEY_WAS_FORCE_SET": "Hashmap key !key was force set to !value.",
    "FILE_IS_MISSING": "!file is missing. Downloading.",
    "CONNECTING_TO_GITHUB": "Connecting to GitHub servers...",
    "TEMP_FOLDER_EXIT": "Installer has detected itself running in temp folder.\n Please unpack cheat first, then run "
                        "the installer once again from the unpacked folder.",
    "CLONING_INTO": "Cloning into: !new_dir",
    "COMMIT_DIFF_RESULTS": "There were !ahead_commits commits since downloading your cheat version. Here are last "
                           "!last_count commits:",
    "DOWNLOADING_NEW_VERSION": "Downloading new update.",
    "NEW_VERSION_AVAILABLE_INPUT": "New version is available, we highly recommend having your cheat up to date. Do "
                                   "you want to update your cheat now?\nOld version: !origin_version, new version: "
                                   "!remote_version",
    "FOLDER_ALREADY_EXIST_INPUT": "Folder: !new_path found. Would you like to delete it?",
    "BRANCH_TO_DOWNLOAD": "Choose branch to download",
    "DAYS_AGO": "!days days ago",
    "FOLDER_DELETED": "Folder deleted successfully. Downloading...",
    "DOWNLOADING_FINISHED": "Downloading finished.",
    "MOVING_CFGS": "[Migration] Moving CFGS",
    "MOVING_HITSOUNDS": "[Migration] Moving HitSounds",
    "MOVING_NADEHELPERS": "[Migration] Moving NadeHelpers",
    "MOVING_DEFAULT_SETTINGS": "[Migration] Moving default settings",
    "DELETE_FOLDER_AFTER_BUILDING_INPUT": "Do you want to delete previous cheat folder after building?",
    "DOWNLOADING_JDK": "Downloading JDK...",
    "BUILDING": "Building RatPoison...",
    "RANDOMIZE_FILE_NAMES_INPUT": "Would you like to randomize the file name for safety?",
    "START_CHEAT_INPUT": "Do you want to start the cheat?",
    "OUTDATED_WINVER_WARNING": "[WARNING] Your operating system is not officially supported by RatPoison. You could "
                               "experience various bugs that will never be fixed. Proceed with caution. "
}


class NetworkedDict(object):
    def make_request(self, should_return="none"):
        try:
            request = requests.get(self.url)
            return None if request.status_code == 404 else request.json()
        except (json.JSONDecodeError, requests.ConnectTimeout, requests.exceptions.ConnectionError, urllib.error.URLError):
            return None if should_return == "none" else {}

    def load_from_file(self, should_return="none"):
        try:
            with open(self.path, encoding="utf_8_sig") as fr:
                return json.loads(fr.read())
        except (json.JSONDecodeError, UnicodeDecodeError, FileNotFoundError):
            return None if should_return == "none" else {}

    def __getitem__(self, key):
        if (tmp_key := self.content.get(key)) is not None:
            return tmp_key
        elif (tmp_key := self.load_from_file("dict").get(key)) is not None:
            return tmp_key
        elif (tmp_key := self.make_request("dict").get(key)) is not None:
            return tmp_key
        elif (tmp_key := self.default_dict.get(key)) is not None:
            return tmp_key
        else:
            raise KeyError(f"Key {key} was not found in any object.")
    
    def __setitem__(self, key, value):
        self.content[key] = value
        with open(self.path, "w") as fw:
            json.dump(self.content, fw, indent=4)
        locales.adv_print(f"KEY_WAS_FORCE_SET", variables={"key": key, "value": value})
    
    def setKey(self, key, value, printMessage=True):
        self.content[key] = value
        with open(self.path, "w") as fw:
            json.dump(self.content, fw, indent=4)
        if (printMessage): locales.adv_print(f"KEY_WAS_FORCE_SET", variables={"key": key, "value": value})
        pass

    def __init__(self, path: typing.AnyStr, url: typing.AnyStr, default_dict: typing.Dict):
        """
        @param path: path to expected file
        @param url: url to get json from if file doesn't exist
        @param default_dict: default dictionary of file if we are unable to connect to the network
        """
        self.path = path
        self.url = url
        self.content = None
        self.default_dict = default_dict
        if os.path.exists(self.path) and (loaded := self.load_from_file()) is not None:
            self.content = loaded
        elif (requested := self.make_request()) is not None:
            self.content = requested
        else:
            self.content = default_dict


class Locales(NetworkedDict):
    def __init__(self, *args: typing.Iterable[typing.Any], **kwargs):
        super().__init__(*args, **kwargs)

    def adv_print(self, message, *args, variables={}, **kwargs):
        message = self.message(message, variables)
        print(message, *args, **kwargs)

    def adv_input(self, message, variables={}, should_lower=True):
        message = self.message(message, variables)
        temp_input = input(f"{message} {self.message('YES_OR_NO')} ")
        return temp_input.lower() if should_lower else temp_input

    @property
    def yes(self):
        return self["YES"]     

    def message(self, key, variables={}):
        r = self[key]
        for gl, gl_val in variables.items():
            if gl in r:
                r = r.replace(f"!{gl}", str(gl_val))
        return r


settings = NetworkedDict("installerSettings.json",
                         "https://raw.githubusercontent.com/SPRAVEDLIVO/RatInstaller/master/installerSettings.json",
                         DEFAULT_SETTINGS)
default_locale = locale.getdefaultlocale()[0]
locales = Locales(f"locales/locale_{default_locale}.json",
                  f"https://raw.githubusercontent.com/retart1337/RatInstaller/master/locales/locale_{default_locale}.json",
                  DEFAULT_LOCALES)