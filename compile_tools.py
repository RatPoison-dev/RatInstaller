from pathlib import Path
import os
import subprocess
import utils
import repository
import settingsTools
import jdk_tools
import requests

locales = settingsTools.locales
settings = settingsTools.settings

repo = repository.Repository(settings['github_repo'])


def compile():
    if settings["download_missing_files"]:
        version = repository.Version.get_version_file()
        repo.compare_tree(version.branch) if version.commit_hash is None else repo.compare_tree(version.commit_hash)
    locales.adv_print("BUILDING")
    if not os.path.exists("gradlew.bat"):
        with open("gradlew.bat", "w") as f:
            f.write(requests.get("https://raw.githubusercontent.com/michel-kraemer/gradle-download-task/master/gradlew.bat").text)
    process = subprocess.Popen(["gradlew.bat", "RatPoison"])
    process.communicate()
    return_code = process.returncode
    utils.kill_jdk()
    if return_code == 0:
        delete_libs_folder()
        bat_file = utils.get_bat_name()
        for path in utils.search_file("java.exe"):
            if utils.verify_path(path):
                java_exe = str(path)
                with open(bat_file, "r") as rFile:
                    prev_lines = rFile.readlines()
                prev_lines[4] = prev_lines[4].replace("java", f"\"{java_exe}\"", 1)
                with open(bat_file, "w") as wFile:
                    wFile.writelines(prev_lines)
                break
        if locales.adv_input("RANDOMIZE_FILE_NAMES_INPUT") in locales.yes:
            randomize_file_names()
        replace_bat_path()
    else:
        if locales.adv_input("RETRY_BUILD_INPUT"):
            settings["skip_jdk_checks"] = False
            settings["force_install_jdk"] = True
            jdk_tools.download_jdk()
            compile()


def delete_libs_folder():
    for path in Path(os.getcwd()).rglob("libs"):
        if len(listdir := os.listdir(str_path := str(path))) > 0 and "RatPoison" in listdir[0]:
            utils.rmtree(str_path)
            break


def randomize_file_names():
    random_name = utils.get_random_name()
    folder_name = utils.get_folder_name()
    for file in os.listdir(folder_name):
        path_to_file = os.path.join(folder_name, file)
        if os.path.isfile(path_to_file):
            file_ext = os.path.splitext(file)[1]
            os.rename(path_to_file, f"{folder_name}/{random_name}{file_ext}")


def replace_bat_path():
    bat_file = utils.get_bat_name()
    with open(bat_file, "r") as rFile:
        prev_lines = rFile.readlines()
    jar_file = utils.get_jar_name()
    prev_lines[4] = f"{' '.join(prev_lines[4].split(' ')[:-3])} \"{jar_file}\"\n"
    with open(bat_file, "w") as wFile:
        wFile.writelines(prev_lines)
