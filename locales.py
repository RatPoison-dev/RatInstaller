import locale
import requests


class Locales(object):
    def init_default_locales(self):
        return {
            "YES": ["y", "yes"],
            "YES_OR_NO": "[Y/N]",
            "CLONING_INTO": "Cloning into: !new_dir",
            "FILE_IS_MISSING": "!file is missing. Downloading.",
            "COMMIT_DIFF_RESULTS": "There were !ahead_commits commits since downloading your cheat version. Here are last !last_count commits:",
            "DOWNLOADING_NEW_VERSION": "Downloading new update.",
            "NEW_VERSION_AVAILABLE_INPUT": "New version is available, we highly recommend having your cheat up to date. Do you want to update your cheat now?\nOld version: !origin_version, new version: !remote_version",
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
            "OUTDATED_WINVER_WARNING": "[WARNING] Your operating system is not officially supported by RatPoison. You could experience various bugs that will never be fixed. Proceed with caution."
        }

    def __init__(self):
        self.default_locale = locale.getdefaultlocale()[0]
        try:
            r = requests.get(
                f"https://raw.githubusercontent.com/retart1337/RatInstaller/master/locales/locale_{self.default_locale}.json")
            if r.status_code == 404:
                self.dict = self.init_default_locales()
            else:
                self.dict = r.json()
        except:
            # No internet connect
            self.dict = self.init_default_locales()

    def advPrint(self, message, *args, globals={}, **kwargs):
        message = self.message(message, globals)
        print(message, *args, **kwargs)

    def advInput(self, message, globals={}, shouldLower=True):
        message = self.message(message, globals)
        tempInput = input(f"{message} {self.message('YES_OR_NO')} ")
        return tempInput.lower() if shouldLower else tempInput

    @property
    def YES(self):
        return self.dict["YES"]

    def message(self, k, globals={}):
        r = self.dict[k] if (k in self.dict) else self.init_default_locales()[k]
        for gl, gl_val in globals.items():
            if gl in r:
                r = r.replace(f"!{gl}", str(gl_val))
        return r
