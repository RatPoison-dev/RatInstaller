import requests, re, random, string, psutil, os
from clint.textui import progress

def downloadFileWithBar(path, link):
    r = requests.get(link, stream=True)
    with open(path, 'wb') as f:
        total_length = int(r.headers.get('content-length'))
        for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
            if chunk:
                f.write(chunk)
                f.flush()

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

def killJDKs():
    for p in psutil.process_iter():
        if ("jdk" in p.name().lower()):
            p.kill()

def searchJDK():
    for file in os.listdir():
        if ("jdk" in file):
            return True
    jdk = os.environ.get("JAVA_HOME")
    # why tf your jdk points to recycle bin bitch are you retarted
    return jdk is not None and verifyPath(jdk)