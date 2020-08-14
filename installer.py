import traceback, os, utils, atexit
def onexit():
    utils.killJDKs()
atexit.register(onexit)
# Crash handler
try:
    import main
except BaseException:
    print("Some exception occured, please report in discord (https://discord.gg/xkTteTM):")
    print("----CUT HERE----")
    traceback.print_exc()
    utils.killJDKs()

os.system("pause")