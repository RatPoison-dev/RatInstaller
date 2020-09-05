import sys, re, locales
WIN_10 = (10, 0, 0)

locales = locales.Locales()


def get_winver():
    wv = sys.getwindowsversion()
    if hasattr(wv, 'service_pack_major'):  # python >= 2.7
        sp = wv.service_pack_major or 0
    else:
        r = re.search(r"\s\d$", wv.service_pack)
        sp = int(r.group(0)) if r else 0
    return (wv.major, wv.minor, sp)

def detectWin():
    if (get_winver() != WIN_10):
        locales.advPrint("OUTDATED_WINVER_WARNING")