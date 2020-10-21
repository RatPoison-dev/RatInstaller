import os
import shutil
import __main__
import locales
import repository
import settingsTools
import utils

settings = settingsTools.load_settings()
locales = locales.Locales()
executing = os.path.splitext(os.path.basename(__main__.__file__))[0]

YES = locales.yes

repo = repository.Repository(settings["github_repo"])


def download_repo(origin_branch):
    locales.adv_print("DOWNLOADING_NEW_VERSION")
    version = repo.get_version(origin_branch).version
    new_path = f"{settings.repository_name} {version}"
    if os.path.exists(new_path):
        if locales.adv_input("FOLDER_ALREADY_EXIST_INPUT", {"new_path": new_path}) in YES:
            utils.rmtree(new_path)
        locales.adv_print("FOLDER_DELETED")
    repo.clone(origin_branch)
    locales.adv_print("DOWNLOADING_FINISHED")
    return new_path


def continue_actions(new_path):
    utils.kill_jdk()
    if os.path.exists("jdk-14.0.2"):
        shutil.move("jdk-14.0.2", new_path)
    locales.adv_print("MOVING_CFGS")
    folder_name = utils.get_settings_path()
    utils.migrate_folder(f"{folder_name}/CFGS", f"{new_path}/settings/CFGS")
    locales.adv_print("MOVING_HITSOUNDS")
    utils.migrate_folder(f"{folder_name}/hitsounds", f"{new_path}/settings/hitsounds")
    locales.adv_print("MOVING_NADEHELPERS")
    utils.migrate_folder(f"{folder_name}/NadeHelper", f"{new_path}/settings/NadeHelper")
    locales.adv_print("MOVING_DEFAULT_SETTINGS")
    utils.migrate_default_settings(f"{folder_name}/", f"{new_path}/settings/CFGS/default_migration.cfg")
    os.chdir(new_path)
    return new_path


def delete_folder(new_path):
    for file in os.listdir("../"):
        file_path = os.path.join("..", file)
        if new_path not in file and executing not in file:
            if os.path.isdir(file_path):
                utils.rmtree(file_path)
            else:
                os.remove(file_path)
    for file in os.listdir(os.getcwd()):
        if ".git" not in file and executing not in file:
            shutil.move(file, "../")
    os.chdir("../")
    utils.rmtree(new_path)


def should_update():
    ask_update = False
    origin = repository.Version.get_version_file()
    # commit compare
    if origin.branch is not None:
        remote_hash = repo.get_latest_commit_hash(origin.branch)
        if origin.commit_hash is not None and remote_hash is not None and origin.commit_hash != remote_hash:
            repo.diff_commits(origin.commit_hash, remote_hash)
            ask_update = True
        remote = repo.get_version(origin.branch)
        if origin.version is not None and remote is not None and origin.version != remote.version:
            ask_update = True
        update = settings["force_cheat_update"] or (locales.adv_input("NEW_VERSION_AVAILABLE_INPUT", globals={
            "origin_version": origin.version, "remote_version": remote.version}) in YES) if ask_update else False
        update = update or settings["force_cheat_update"]
        return update, origin.branch
