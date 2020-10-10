import os
import shutil
import __main__
import locales
import repository
import settingsTools
import utils

settings = settingsTools.loadSettings()
locales = locales.Locales()
executing = os.path.splitext(os.path.basename(__main__.__file__))[0]

YES = locales.YES

repo = repository.Repository(settings["github_repo"])


def download_repo(origin_branch):
    locales.advPrint("DOWNLOADING_NEW_VERSION")
    version = repo.get_version(origin_branch).version
    new_path = f"{settings.repository_name} {version}"
    if (os.path.exists(new_path)):
        if (locales.advInput("FOLDER_ALREADY_EXIST_INPUT", {"new_path": new_path}) in YES):
            utils.rmtree(new_path)
        locales.advPrint("FOLDER_DELETED")
    repo.clone(origin_branch)
    locales.advPrint("DOWNLOADING_FINISHED")
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
        if not new_path in file and not executing in file:
            if os.path.isdir(filePath):
                utils.rmtree(filePath)
            else:
                os.remove(filePath)
    for file in os.listdir(os.getcwd()):
        if not ".git" in file and not executing in file:
            shutil.move(file, "../")
    os.chdir("../")
    utils.rmtree(new_path)

def shouldUpdate():
    should_update = False
    askupdate = False
    origin = repository.Version.get_version_file()
    #commit compare
    if origin.commit_hash is not None and origin.commit_hash != (remote_hash := repo.get_latest_commit_hash(origin.branch)):
        repo.diff_commits(origin.commit_hash, remote_hash)
        askupdate = True
    if origin.version is not None and origin.version != (remote := repo.get_version(origin.branch)).version:
        askupdate = True
    should_update = settings["force_cheat_update"] or (locales.advInput("NEW_VERSION_AVAILABLE_INPUT", globals={
        "origin_version": origin.version, "remote_version": remote.version}) in YES) if askupdate else False
    return should_update, origin.branch