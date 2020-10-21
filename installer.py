import atexit
import locales
import os
import settingsTools
import traceback
import utils
from whaaaaat import print_json

settings = settingsTools.load_settings()
locales = locales.Locales()

can_continue = True
if os.environ["TEMP"] in os.getcwd():
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
        print("Some exception occured, please report in discord (https://discord.gg/xkTteTM):")
        print("----CUT HERE----")
        print("Installer settings:")
        print_json(settings.dict)
        traceback.print_exc()
        utils.kill_jdk()

os.system("pause")
