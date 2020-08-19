import traceback, os, utils, atexit, settingsTools
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
    print(f"Installer settings: {settings}\n\n")
    traceback.print_exc()
    utils.killJDKs()

os.system("pause")