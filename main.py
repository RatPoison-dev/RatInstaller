import __main__
import os
import subprocess
import whaaaaat
import winver
import repository
import settingsTools
import compile_tools
import jdk_tools
import utils
import update
import sys
YES = settingsTools.locales.yes
locales = settingsTools.locales
settings = settingsTools.settings
winver.detect_win()
executing = utils.get_main()
repo = repository.Repository(settings['github_repo'])
args = sys.argv[1:]

def run_continue_update_loop(folder_path):
    update.continue_actions(folder_path)
    if folder_path is not None and locales.adv_input("DELETE_FOLDER_AFTER_BUILDING_INPUT") in YES:
        update.delete_folder(folder_path)
    compile_tools.compile()
    version_file = repository.Version.get_version_file()
    version_file.write_commit_hash(repo.get_latest_commit_hash(version_file.branch))
    utils.ask_start_cheat()

using_correct_repo = True

try:
    process = subprocess.Popen("git diff --name-only", stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, encoding = "UTF-8")
    out, err = process.communicate()
    if process.returncode == 0:
        # git is available & has changes
        if len([x for x in out.split("\n") if x]) > 0:
            p = subprocess.Popen("git config --get remote.origin.url", stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, encoding = "UTF-8")
            out2, _ = p.communicate()
            # editing ratpoison repository
            if out2.endswith(f"{repo.repository_name}.git\n"):
                settings.setKey("download_missing_files", False, False)
                print("Downloading missing files disabled due to developer mode. Enjoy ;)")
            else:
                using_correct_repo = False
except: 
    pass

CD = args[0] if len(args) > 0 else "False"
PATH = args[1] if len(args) > 1 else ""

if CD == "True":
    run_continue_update_loop(PATH)
else:
    if not jdk_tools.search_jdk() or settings["force_install_jdk"] or True:
        jdk_tools.download_jdk()
    # Update checks only when the
    if using_correct_repo and (installed := utils.get_installed_state()):
        if builded := utils.get_build_state():
            shouldUpdate, origin_branch = update.should_update()
            if shouldUpdate:
                if not settings["bypass_download"]:
                    generated_folder_path = update.download_repo(origin_branch)
                else:
                    generated_folder_path = ""
                    for i in os.listdir():
                        if repo.repository_name in i and os.path.isdir(i) and "version.txt" in os.listdir(i):
                            generated_folder_path = i
                            break
                    if generated_folder_path == "":
                        raise Exception("RatPoison folder was not found")
                if settings["update_type"] == "call_installer":
                    call = f"{generated_folder_path}/{executing}.exe" if os.path.exists(f"{generated_folder_path}/{executing}.exe") else f"{generated_folder_path}/{executing}.bat"
                    subprocess.check_call(
                        f"{call} True \"{generated_folder_path}\"")
                    os._exit(0)
                else:
                    run_continue_update_loop(generated_folder_path)
            elif not settings["force_cheat_compile"]:
                utils.ask_start_cheat()
        if not builded or settings["force_cheat_compile"]:
            compile_tools.compile()
            utils.ask_start_cheat()
    else:
        if utils.test_internet_connection():
            locales.adv_print("CONNECTING_TO_GITHUB")
            branches = repo.get_branches()
            questions = [
                {
                    'type': 'list',
                    'name': 'branch',
                    'message': locales.message("BRANCH_TO_DOWNLOAD"),
                    'choices': list(branches)
                }
            ]
            answers = whaaaaat.prompt(questions)
            raw_branch = answers.get('branch')
            commit_hash = branches[raw_branch]["sha"]
            branch = raw_branch.split()[0]
            version = repo.get_version(branch)
            if version is None: 
                locales.adv_print("FETCH_VERSION_FAILED")
                os.system("pause")
                os._exit(0)
            version = version.version
            new_dir = f"{repo.repository_name} {version}"
            locales.adv_print("CLONING_INTO", variables={"new_dir": new_dir})
            repo.clone(branch)
            os.chdir(new_dir)
            repository.Version.get_version_file().write_commit_hash(commit_hash)
            if os.path.exists(f"{executing}.bat"):
                subprocess.check_call(f"{executing}.bat")
                os._exit(0)
            elif os.path.exists(f"{executing}.exe"):
                subprocess.check_call(f"{executing}.exe")
                os._exit(0)
