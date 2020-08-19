import subprocess, string, random, requests, zipfile, os, glob, shutil, pygit2, re, utils, settingsTools, winver
from clint.textui import progress
from pathlib import Path
import __main__

settings = settingsTools.loadSettings()

executing = os.path.splitext(os.path.basename(__main__.__file__))[0]

winver.detectWin()

installed = False
updated = False
createdTask = False
YES = ["y", "yes", "YES", "Y"]
JDK_LINK = "https://download.java.net/java/GA/jdk14.0.2/205943a0976c4ed48cb16f1043c5c647/12/GPL/openjdk-14.0.2_windows-x64_bin.zip"
JDK_ZIP_NAME = "JDK.zip"

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


def migrateFolder(folder):
    for f in os.listdir(folder):
        prev_path = f"{folder}/{f}"
        if (os.path.isfile(prev_path)):
            shutil.move(prev_path, f"{new_path}/{folder}/{f}")

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
            if (remote_version != origin_version and (input("New version is available, we highly recommend having your cheat up to date. Do you want to update your cheat now? [Y/N] ") in YES or settings["force_cheat_update"])):
                print(f"Cheat is outdated, downloading new update.\nOld version: {origin_version}, new version: {remote_version}")
                new_path = f"RatPoison-{origin_branch}"
                if (os.path.exists(new_path)):
                    if (input(f"Folder: {new_path} found. Would you like to delete it? [Y/N] ").lower() in YES):
                        shutil.rmtree(new_path, ignore_errors=True)
                updated = True
                pygit2.clone_repository(f"https://github.com/TheFuckingRat/RatPoison.git", new_path, checkout_branch=origin_branch)
                utils.killJDKs()
                if (os.path.exists("jdk-14.0.2")):
                    shutil.move("jdk-14.0.2", new_path)

                print("[Migration] Moving CFGS")
                migrateFolder("settings/CFGS")
                print("[Migration] Moving HitSounds")
                migrateFolder("settings/hitsounds")
                print("[Migration] Moving NadeHelpers")
                migrateFolder("settings/NadeHelper")
                print("[Migration] Moving default settings")
                migrateFolder("settings/")
                os.chdir(new_path)
                i = input("Do you want to delete previous cheat folder after building? [Y/N] ").lower()
                if (i.lower() in YES):
                    createdTask = True

        else:
            print("Specified branch is probably invalid.")
    break

def startCheat():
    subprocess.run([bat_file])

if (not utils.searchJDK() or settings["force_install_jdk"] == True):
    print("Downloading JDK...")
    utils.downloadFileWithBar(JDK_ZIP_NAME, JDK_LINK)
    with zipfile.ZipFile(JDK_ZIP_NAME) as zip_ref:
        zip_ref.extractall("")
    os.remove(JDK_ZIP_NAME)
    # Set JAVA_HOME and PATH
    utils.setJavaHome("jdk-14.0.2")
    os.environ["PATH"] = os.environ["PATH"]+";"+os.path.join(os.environ["JAVA_HOME"], "bin")

if (not installed or updated):
    # BUILD
    print("Building RatPoison...")
    subprocess.check_call(["gradlew.bat", "RatPoison"])
    utils.killJDKs()
    setFolder()
    if (input("Would you like to randomize the file name for safety? [Y/N] ").lower() in YES):
        random_name = utils.getRandomName()
        setFolder()
        for file in os.listdir(folder_name):
            path_to_file = os.path.join(folder_name, file)
            if (os.path.isfile(path_to_file)):
                fileExt = os.path.splitext(file)[1]
                os.rename(path_to_file, f"{folder_name}/{random_name}{fileExt}")
    if (createdTask):
        # Delete folder above 
        for file in os.listdir("../"):
            filePath = os.path.join("..", file)
            if (not new_path in file and not executing in file):
                if (os.path.isdir(filePath)):
                    shutil.rmtree(filePath, ignore_errors=True)
                else:
                    os.remove(filePath)
        for file in os.listdir(os.getcwd()):
            if (not ".git" in file and not executing in file):
                shutil.move(file, "../")
        os.chdir("../")
        setFolder()
        shutil.rmtree(new_path, ignore_errors=True)

    setFolder()
    with open(bat_file, "r") as rFile:
        prevLines = rFile.readlines()
    prevLines[4] = f"{' '.join(prevLines[4].split(' ')[:-3])} \"{jar_file}\"\n"
    with open(bat_file, "w") as wFile:
        wFile.writelines(prevLines)


    pathToSearch = os.environ["JAVA_HOME"] if os.environ.get("JAVA_HOME") is not None and utils.verifyPath(os.environ["JAVA_HOME"]) else os.path.splitdrive(os.getcwd())[0]+"/"
    for path in utils.searchFile("java.exe"):
        if (utils.verifyPath(str(path))):
            setFolder()
            java_exe = str(path)
            with open(bat_file, "r") as rFile:
                prevLines = rFile.readlines()
            prevLines[4] = prevLines[4].replace("java", f"\"{java_exe}\"", 1)
            with open(bat_file, "w") as wFile:
                wFile.writelines(prevLines)
            break
    if (input("Do you want to start the cheat? [Y/N] ").lower() in YES):
        startCheat()

else:
    startCheat()

