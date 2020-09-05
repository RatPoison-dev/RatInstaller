import requests, re, random, string, psutil, os, sys, subprocess, stat, threading, time, pyspeedtest, locales
from pathlib import Path
from clint.textui import progress

sendKeepAliveMessage = False
locales = locales.Locales()

def downloadFileWithBar(path, link):
    r = requests.get(link, stream=True)
    with open(path, 'wb') as f:
        total_length = int(r.headers.get('content-length'))
        for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
            if chunk:
                f.write(chunk)
                f.flush()

def on_rm_error(func, path, exc_info):
    os.chmod(path, stat.S_IWRITE)
    os.unlink(path)

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
    for path in searchFile("jps.exe"):
        strPath = str(path)
        processes = [int(x) for x in subprocess.getoutput(f"\"{strPath}\" -q").split("\n")]
        for process in processes:
            try:
                os.kill(process, 0)
            except:
                pass
        break

def setJavaHome(path):
    os.environ["JAVA_HOME"] = os.path.join(os.getcwd(), path)

def sendKeepAlive():
    st = pyspeedtest.SpeedTest("google.com")
    speed = st.download()/1024/1024
    while sendKeepAliveMessage:
        locales.advPrint("DOWNLOADING_REPO_KEEP_ALIVE", globals={"speed":speed})
        time.sleep(5)

def startKeepAliveThread():
    global sendKeepAliveMessage
    sendKeepAliveMessage = True
    threading.Thread(target=sendKeepAlive, name="Keep-Alive").start()

def searchJDK():
    for file in os.listdir():
        if ("jdk" in file):
            setJavaHome(file)
            return True
    jdk = os.environ.get("JAVA_HOME")
    # why tf your jdk points to recycle bin bitch are you retarted
    return jdk is not None and verifyPath(jdk)