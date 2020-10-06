import glob, requests, settingsTools, locales, os, subprocess, shutil, utils, pygit2, __main__
settings = settingsTools.loadSettings()
locales = locales.Locales()
executing = os.path.splitext(os.path.basename(__main__.__file__))[0]

YES = locales.YES

repository = settings["github_repo"]

def download_repo(origin_version, remote_version, origin_branch):
    locales.advPrint("DOWNLOADING_NEW_VERSION", globals={"origin_version": origin_version, "remote_version": remote_version})
    new_path = f"RatPoison-{origin_branch}"
    if (os.path.exists(new_path)):
        if (locales.advInput("FOLDER_ALREADY_EXIST_INPUT", {"new_path": new_path}) in YES):
            shutil.rmtree(new_path, onerror=utils.on_rm_error)
        locales.advPrint("FOLDER_DELETED")
    utils.startKeepAliveThread()
    pygit2.clone_repository(f"https://github.com/{repository}.git", new_path, checkout_branch=origin_branch)
    locales.advPrint("DOWNLOADING_FINISHED")
    utils.sendKeepAliveMessage = False
    return new_path

def continue_actions(new_path):
    utils.killJDKs()
    if (os.path.exists("jdk-14.0.2")):
        shutil.move("jdk-14.0.2", new_path)
    locales.advPrint("MOVING_CFGS")
    folder_name = utils.getSettingsPath()
    utils.migrateFolder(f"{folder_name}/CFGS", f"{new_path}/settings/CFGS")
    locales.advPrint("MOVING_HITSOUNDS")
    utils.migrateFolder(f"{folder_name}/hitsounds", f"{new_path}/settings/hitsounds")
    locales.advPrint("MOVING_NADEHELPERS")
    utils.migrateFolder(f"{folder_name}/NadeHelper", f"{new_path}/settings/NadeHelper")
    locales.advPrint("MOVING_DEFAULT_SETTINGS")
    utils.migrateDefaultSettings(f"{folder_name}/", f"{new_path}/settings/CFGS/default_migration.cfg")
    os.chdir(new_path)
    return new_path

def delete_folder(new_path):
    for file in os.listdir("../"):
        filePath = os.path.join("..", file)
        if (not new_path in file and not executing in file):
            if (os.path.isdir(filePath)):
                utils.rmtree(filePath)
            else:
                os.remove(filePath)
    for file in os.listdir(os.getcwd()):
        if (not ".git" in file and not executing in file):
            shutil.move(file, "../")
    os.chdir("../")
    utils.rmtree(new_path)

def shouldUpdate():
    for file in glob.glob("version.txt"):
        with open(file) as f:
            c = f.readlines()
            origin_version = c[0].replace("\n", "")
            origin_branch = c[1].replace("\n", "")
            r = requests.get(f"https://raw.githubusercontent.com/{repository}/{origin_branch}/version.txt")
            if (r.status_code == 404):
                return False, 0, 0, 0
            remote_text = r.text.split("\n")
            remote_version = remote_text[0]
            if (remote_version == origin_version):
                return False, 0, 0, 0
            shouldUpdate = settings["force_cheat_update"] or (locales.advInput("NEW_VERSION_AVAILABLE_INPUT") in YES)
            if (not shouldUpdate):
                return False, 0, 0, 0
            return True, origin_version, remote_version, origin_branch
    return False, 0, 0, 0