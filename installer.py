import subprocess, string, random, requests, zipfile, os, glob, shutil, pygit2, re, psutil
from clint.textui import progress
from pathlib import Path

installed = False
updated = False
createdTask = False

def downloadFileWithBar(path, link):
    r = requests.get(link, stream=True)
    with open(path, 'wb') as f:
        total_length = int(r.headers.get('content-length'))
        for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
            if chunk:
                f.write(chunk)
                f.flush()

def killJDKs():
    for p in psutil.process_iter():
        if ("jdk" in p.name().lower()):
            p.kill()

def setFolder():
    global installed, raw_folder_name, folder_name, bat_file, jar_file
    if os.path.exists("build/"):
        for file in os.listdir("build/"):
            if ("RatPoison" in file):
                installed = True
                raw_folder_name = file
                folder_name = os.path.join("build", raw_folder_name)
                for file in os.listdir(folder_name):
                    if (".bat" in file): bat_file = os.path.join(folder_name, file)
                    elif (".jar" in file): jar_file = file

setFolder()

def searchJDK():
    for file in os.listdir():
        if ("jdk" in file):
            return True
    jdk = os.environ.get("JAVA_HOME")
    # why tf your jdk points to recycle bin bitch are you retarted
    return jdk is not None and verifyPath(jdk)

def parseJDKVersion(path):
    try:
        return int(re.findall(r"jdk-\d+", path.lower())[0].split("jdk-")[1])
    except:
        return None

def verifyPath(path):
    return not "jre" in path.lower() and parseJDKVersion(path) is not None and parseJDKVersion(path) >= 12 and not "$RECYCLE.BIN" in path


def migrateFolder(folder):
    for f in os.listdir(folder):
        shutil.move(os.path.join(folder, f), os.path.join(new_path, folder, f))

for file in glob.glob("version.txt"):
    # Autoupdate
    with open(file) as f:
        c = f.readlines()
        origin_version = c[0].replace("\n", "")
        origin_branch = c[1].replace("\n", "")
        r = requests.get(f"https://raw.githubusercontent.com/TheFuckingRat/RatPoison/{origin_branch}/version.txt")
        if (r.status_code != 404):
            remote_text = r.text.split("\n")
            remote_version = remote_text[0]
            if (remote_version != origin_version):
                updated = True
                print("Versions doesn't match. Redownloading RatPoison")
                new_path = f"RatPoison-{origin_branch}/"
                pygit2.clone_repository(f"https://github.com/TheFuckingRat/RatPoison.git", new_path, checkout_branch=origin_branch)
                if (os.path.exists("jdk-14.0.2")):
                    shutil.move("jdk-14.0.2", new_path)

                print("[Migration] Moving CFGS")
                migrateFolder("settings/CFGS")
                print("[Migration] Moving HitSounds")
                migrateFolder("settings/hitsounds")
                print("[Migration] Moving NadeHelpers")
                migrateFolder("settings/NadeHelper")
                os.chdir(new_path)
                i = input("Do you want to delete previos cheat folder after building? [Y/N] ").lower()
                if (i.lower() in ["y", "yes"]):
                    createdTask = True

        else:
            print("Specified branch is probably invalid.")
    break

JDK_LINK = "https://download.java.net/java/GA/jdk14.0.2/205943a0976c4ed48cb16f1043c5c647/12/GPL/openjdk-14.0.2_windows-x64_bin.zip"
JDK_ZIP_NAME = "JDK.zip"

def startCheat():
    # Нет блять пошел нахуй руками запускай тупой пендос ленивый, мразь сука конченная, уёбок блять, запускай давай пидарас
    subprocess.run([bat_file])

def getRandomName():
    s = ""
    for _ in range(20):
        s += random.choice(string.ascii_uppercase)
    return s

if (not searchJDK()):
    print("Downloading JDK...")
    downloadFileWithBar(JDK_ZIP_NAME, JDK_LINK)
    with zipfile.ZipFile(JDK_ZIP_NAME) as zip_ref:
        zip_ref.extractall("")
    os.remove(JDK_ZIP_NAME)
    # Set JAVA_HOME and PATH
    os.environ["JAVA_HOME"] = os.path.join(os.getcwd(), "jdk-14.0.2")
    os.environ["PATH"] = os.environ["PATH"]+";"+os.path.join(os.environ["JAVA_HOME"], "bin")

if (not installed or updated):
    # BUILD
    print("Building RatPoison...")
    subprocess.check_call(["gradlew.bat", "RatPoison"])
    killJDKs()
    setFolder()
    if (input("Would you like to randomize the file name for safety? [Y/N] ").lower() in ["y", "yes"]):
        random_name = getRandomName()
        setFolder()
        for file in os.listdir(folder_name):
            path_to_file = os.path.join(folder_name, file)
            if (os.path.isfile(path_to_file)):
                fileExt = os.path.splitext(file)[1]
                os.rename(path_to_file, f"{folder_name}/{random_name}{fileExt}")
    #Fuck this
    #if (createdTask):
    #    curPath = os.getcwd()
    #    shutil.move(curPath, "../")
    #    setFolder()
    drive = os.path.splitdrive(os.getcwd())[0]+"/"
    for path in Path(drive).rglob('java.exe'):
        if (verifyPath(str(path))):
            setFolder()
            java_exe = str(path)
            with open(bat_file, "r") as rFile:
                prevLines = rFile.readlines()
            prevLines[4] = f'\t\t"{java_exe}" -Xmx512m -Xms32m -XX:+UseSerialGC -jar "{jar_file}"\n'
            with open(bat_file, "w") as wFile:
                wFile.writelines(prevLines)
            break
    if (input("Do you want to start the cheat? [Y/N] ").lower() in ["y", "yes"]):
        startCheat()

else:
    startCheat()

os.system("pause")