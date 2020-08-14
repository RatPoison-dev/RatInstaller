import traceback, os

# Crash handler
try:
    import main
except:
    print("Some exception occured, please report in discord (https://discord.gg/xkTteTM):")
    print("----CUT HERE----")
    traceback.print_exc()
    
os.system("pause")