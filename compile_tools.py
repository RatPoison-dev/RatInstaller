from pathlib import Path
import locales
import os
import subprocess
import utils
import repository
import settingsTools

locales = locales.Locales()
settings = settingsTools.loadSettings()

repo = repository.Repository(settings['github_repo'])

def compile():
    version = repository.Version.get_version_file()
    repo.compare_tree(version.branch) if version.commit_hash is None else repo.compare_tree(version.commit_hash)
    locales.advPrint("BUILDING")
    subprocess.check_call(["gradlew.bat", "RatPoison"])
    deleteLibsFolder()
    utils.killJDKs()
    bat_file = utils.getBatName()
    for path in utils.searchFile("java.exe"):
        if utils.verifyPath(str(path)):
            java_exe = str(path)
            with open(bat_file, "r") as rFile:
                prevLines = rFile.readlines()
            prevLines[4] = prevLines[4].replace("java", f"\"{java_exe}\"", 1)
            with open(bat_file, "w") as wFile:
                wFile.writelines(prevLines)
            break
    if locales.advInput("RANDOMIZE_FILE_NAMES_INPUT") in locales.YES:
        randomize_file_names()
    replace_bat_pathes()

def deleteLibsFolder():
    for path in Path(os.getcwd()).rglob("libs"):
        if len(listdir := os.listdir(strpath := str(path))) > 0 and "RatPoison" in listdir[0]:
            utils.rmtree(strpath)
            break


def randomize_file_names():
    random_name = utils.getRandomName()
    folder_name = utils.getFolderName()
    for file in os.listdir(folder_name):
        path_to_file = os.path.join(folder_name, file)
        if os.path.isfile(path_to_file):
            fileExt = os.path.splitext(file)[1]
            os.rename(path_to_file, f"{folder_name}/{random_name}{fileExt}")
    
def replace_bat_pathes():
    bat_file = utils.getBatName()
    with open(bat_file, "r") as rFile:
        prevLines = rFile.readlines()
    jar_file = utils.getJarName()
    prevLines[4] = f"{' '.join(prevLines[4].split(' ')[:-3])} \"{jar_file}\"\n"
    with open(bat_file, "w") as wFile:
        wFile.writelines(prevLines)