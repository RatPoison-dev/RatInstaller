import settingsTools
import sys

WINVERS = (10, 11)

locales = settingsTools.locales


def get_win_ver():
    wv = sys.getwindowsversion()
    return wv.major


def detect_win():
    if get_win_ver() not in WINVERS:
        locales.adv_print("OUTDATED_WINVER_WARNING")
