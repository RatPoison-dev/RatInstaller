import shutil, utils, settingsTools, winver, locales, jdk_tools, update, compile_tools, argparse, os, subprocess, __main__, exceptions, whaaaaat
from clint.textui import progress
from pathlib import Path
locales = locales.Locales()
YES = locales.YES
settings = settingsTools.loadSettings()
winver.detectWin()
executing = os.path.splitext(os.path.basename(__main__.__file__))[0]

parser = argparse.ArgumentParser()
parser.add_argument("--cd", default="False", help="Installer's variable to communicate with spawned installer after update. Don't edit manually.")
parser.add_argument("--path", default=None, help="Installer's variable to communicate with spawned installer after update. Don't edit manually.")
args = parser.parse_args()

def runContinueUpdateLoop(generated_folder_path):
    update.continue_actions(generated_folder_path)
    if (generated_folder_path is not None and locales.advInput("DELETE_FOLDER_AFTER_BUILDING_INPUT") in YES):
        update.delete_folder(generated_folder_path)
    compile_tools.compile()
    utils.askStartCheat()

if args.cd == "True":  
    runContinueUpdateLoop(args.path)
else:
    if (not jdk_tools.searchJDK() or settings["force_install_jdk"] == True):
        jdk_tools.downloadJDK()
    # Update checks only when builded
    if installed := utils.getInstalledState():
        if builded := utils.getBuildedState():
            shouldUpdate, origin_version, remote_version, origin_branch = update.shouldUpdate()
            if shouldUpdate:
                if (not settings["bypass_download"]):
                    generated_folder_path = update.download_repo(origin_branch)
                else:
                    generated_folder_path = ""
                    for i in os.listdir():
                        if settings.repository_name in i and os.path.isdir(i) and "version.txt" in os.listdir(i): 
                            generated_folder_path = i
                            break
                    if generated_folder_path == "": raise exceptions.BypassDownloadError("RatPoison folder was not found")
                if settings["update_type"] == "call_installer":
                    subprocess.check_call(f"{generated_folder_path}/{executing}.exe --cd=True --path={generated_folder_path}")
                    os._exit(0)
                else:
                    runContinueUpdateLoop(generated_folder_path)
            elif not settings["force_cheat_compile"]:
                utils.askStartCheat()
        elif not builded or settings["force_cheat_compile"]:
            compile_tools.compile()
            utils.askStartCheat()
    else:
        if utils.testInternetConnection():
            questions = [
                {
                    'type': 'list',
                    'name': 'branch',
                    'message': locales.message("BRANCH_TO_DOWNLOAD"),
                    'choices': utils.getRepositoryBranches(settings['github_repo'])
                }
            ]
            answers = whaaaaat.prompt(questions)
            branch = answers.get('branch').split()[0]
            new_dir = f"{settings.repository_name}-{branch}"
            utils.downloadFileAndExtract(f"https://github.com/{settings['github_repo']}/archive/{branch}.zip", f"{branch}.zip")
            os.chdir(new_dir)
            if os.path.exists(f"{executing}.exe"):
                subprocess.check_call(f"{new_dir}/{executing}.exe")
                os._exit(0)