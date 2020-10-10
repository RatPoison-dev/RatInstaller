import traceback, os, utils, atexit, settingsTools
from whaaaaat import print_json

settings = settingsTools.loadSettings()


def onexit():
    utils.killJDKs()


atexit.register(onexit)
# Crash handler
try:
    import main
except BaseException:
    print("Some exception occured, please report in discord (https://discord.gg/xkTteTM):")
    print("----CUT HERE----")
    print("Installer settings:")
    print_json(settings.dict)
    traceback.print_exc()
    utils.killJDKs()

os.system("pause")
