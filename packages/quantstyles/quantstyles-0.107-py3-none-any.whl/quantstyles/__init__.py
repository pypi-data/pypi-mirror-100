from . import quantcmaps
import os


def _copy_style():
    print("Installing matplotlib styles...")
    import os
    import matplotlib
    from pathlib import Path
    from pkg_resources import resource_string

    files = [
        'stylelib/quant.mplstyle',
    ]

    for fname in files:
        path = os.path.join(matplotlib.get_configdir(), fname)
        Path(os.path.dirname(path)).mkdir(parents=True, exist_ok=True)
        text = resource_string(__name__, fname).decode()
        open(path, 'w').write(text)

    with open(__flagpath, "w") as f:
        f.write("1")


__flagpath = os.path.dirname(__file__) + os.path.sep + "style_installed.flag"

if os.path.exists(__flagpath):
    with open(__flagpath, "r") as f:
        flag = f.read(1)
    if flag == "0":
        _copy_style()
else:
    _copy_style()
