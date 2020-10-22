import re
import settingsTools
import sys

WIN_10 = (10, 0, 0)

locales = settingsTools.locales


def get_win_ver():
    wv = sys.getwindowsversion()
    if hasattr(wv, 'service_pack_major'):  # python >= 2.7
        sp = wv.service_pack_major or 0
    else:
        r = re.search(r"\s\d$", wv.service_pack)
        sp = int(r.group(0)) if r else 0
    return wv.major, wv.minor, sp


def detect_win():
    if get_win_ver() != WIN_10:
        locales.adv_print("OUTDATED_WINVER_WARNING")
