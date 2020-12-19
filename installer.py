import atexit
import os
import settingsTools
import traceback
import utils
from whaaaaat import print_json

settings = settingsTools.settings
locales = settingsTools.locales

can_continue = True
if utils.is_running_from_zip():
    locales.adv_print("TEMP_FOLDER_EXIT")
    can_continue = False


def on_exit():
    utils.kill_jdk()


atexit.register(on_exit)
# Crash handler
if can_continue:
    try:
        import main
    except BaseException:
        print("Some exception occurred, please report in discord (https://dimden.dev/ratpoisonowns):")
        print("----CUT HERE----")
        print("Installer settings:")
        print_json(settings.content)
        traceback.print_exc()
        utils.kill_jdk()

os.system("pause")
