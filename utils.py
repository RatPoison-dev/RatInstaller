import requests, re, random, string, psutil, os, sys, subprocess, stat, threading, time, pyspeedtest, locales, glob, settingsTools, shutil
from pathlib import Path
from clint.textui import progress

settings = settingsTools.loadSettings()

sendKeepAliveMessage = False
locales = locales.Locales()

def getInstalledState():
    if (folder_name := getFolderName()) == None: return False
    for _ in Path(folder_name).rglob("*.bat"):
        return True
    return False

def getFolderName():
    if not os.path.exists(settings["build_folder"]): return None
    for file in Path(settings["build_folder"]).rglob("*.bat"):
        return str(file.parent)
    return None

def getBatName():
    if not os.path.exists(settings["build_folder"]): return None
    folder_name = getFolderName()
    for file in Path(folder_name).rglob("*.bat"):
        return str(file)

def getSettingsPath():
    for file in os.listdir(getFolderName()):
        if (os.path.exists(os.path.join(file, "CFGS"))):
            return file

def getJarName():
    if not os.path.exists(settings["build_folder"]): return None
    folder_name = getFolderName()
    for file in Path(folder_name).rglob("*.jar"):
        return str(file.name)


def startCheat():
    bat_file = getBatName()
    subprocess.run([bat_file])

def migrateDefaultSettings(folder, savePath):
    cfg = ""
    for file in os.listdir(folder):
        prevpath = os.path.join(folder, file)
        if os.path.isfile(prevpath):
            with open(prevpath, "r") as fr:
                for line in fr:
                    try:
                        splitted = line.split("=")
                        assert len(splitted) == 2
                        assert not "//" in line
                        cfg += line
                    except AssertionError:
                        pass
    with open(savePath, "w") as fw:
        fw.write(cfg)

def migrateFolder(folder, new_folder):
    for f in os.listdir(folder):
        prev_path = f"{folder}/{f}"
        nwpath = f"{new_folder}/{f}"
        if (os.path.isfile(prev_path)):
            if (os.path.exists(nwpath)):
                os.remove(nwpath)
            shutil.move(prev_path, nwpath)

def downloadFileWithBar(path, link):
    r = requests.get(link, stream=True)
    with open(path, 'wb') as f:
        total_length = int(r.headers.get('content-length'))
        for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
            if chunk:
                f.write(chunk)
                f.flush()

def on_rm_error(func, path, exc_info):
    try:
        subprocess.check_call(f"attrib -H {path}")
        os.chmod(path, stat.S_IWRITE)
        os.unlink(path)
    except:
        pass

def parseJDKVersion(path):
    try:
        return int(re.findall(r"jdk-\d+", path.lower())[0].split("jdk-")[1])
    except:
        return None

def verifyPath(path):
    return not "jre" in path.lower() and parseJDKVersion(path) is not None and parseJDKVersion(path) >= 12 and not "$RECYCLE.BIN" in path

def getRandomName():
    s = ""
    for _ in range(20):
        s += random.choice(string.ascii_uppercase)
    return s

def searchFile(file):
    pathToSearch = os.environ["JAVA_HOME"] if os.environ.get("JAVA_HOME") is not None and verifyPath(os.environ["JAVA_HOME"]) else os.path.splitdrive(os.getcwd())[0]+"/"
    return Path(pathToSearch).rglob(file)

def killJDKs():
    try:
        for path in searchFile("jps.exe"):
            strPath = str(path)
            processes = [int(x) for x in subprocess.getoutput(f"\"{strPath}\" -q").split("\n")]
            for process in processes:
                try:
                    os.kill(process, 0)
                except:
                    pass
            break
    except:
        # Nah
        pass

def setJavaHome(path):
    os.environ["JAVA_HOME"] = os.path.join(os.getcwd(), path)

def sendKeepAlive():
    st = pyspeedtest.SpeedTest("google.com")
    while sendKeepAliveMessage:
        speed = "{:.3f}".format(st.download()/1024/1024)
        locales.advPrint("DOWNLOADING_REPO_KEEP_ALIVE", globals={"speed":speed})
        time.sleep(5)

def startKeepAliveThread():
    global sendKeepAliveMessage
    sendKeepAliveMessage = True
    threading.Thread(target=sendKeepAlive, name="Keep-Alive").start()