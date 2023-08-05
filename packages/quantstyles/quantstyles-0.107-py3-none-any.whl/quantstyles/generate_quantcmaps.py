import numpy as np
import matplotlib.pyplot as plt
import glob
import os

from get_cpt import get_cmap

print("Converting CPTs to .py...")

cmaps = dict()
cmps = []
cmaps["singlecolor"] = []
cmaps["diverging"] = []
cmaps['multicolor'] = []
for file in sorted(glob.glob("./colormaps/*.cpt")):
    cmap = get_cmap(file)
    if ("black" in file) or ("white" in file):
        cmaps['singlecolor'].append(cmap)
    elif "diverging" in file:
        cmaps['diverging'].append(cmap)
    else:
        cmaps['multicolor'].append(cmap)

nrows = max(len(cmap_list) for cmap_category, cmap_list in cmaps.items())
gradient = np.linspace(0, 1, 256)
gradient = np.vstack((gradient, gradient))


def save_to_py(cmap, name, fname):
    data = cmap._segmentdata
    data_repr = repr(data).replace('],', '],\n')
    new = not os.path.isfile(fname)
    with open(fname, "a") as f:
        if new:
            print("from matplotlib.colors import LinearSegmentedColormap", file=f)
            print("import matplotlib.cm as cm", file=f)
        print(f"_{name}_data = {data_repr}\n", file=f)
        print(f"cmap_{name} = LinearSegmentedColormap(\"{name}\", _{name}_data)", file=f)
        print(f"cm.register_cmap(name=\"{name}\", cmap=cmap_{name})", file=f)


def findnth(haystack, needle, n):
    parts = haystack.split(needle, n + 1)
    if len(parts) <= n + 1:
        return -1
    return len(haystack) - len(parts[-1]) - len(needle)


def parse_name(cmap):
    endidx = findnth(cmap.name, "_", 2)
    startidx = findnth(cmap.name, "_", 0)
    nametext = cmap.name[startidx + 1:endidx]
    if any(char.isdigit() for char in nametext):
        nametext = nametext.split("_")[0]
    return nametext


def plot_color_gradients(cmaps):
    nrows = sum([len(cmaps[c]) for c in cmaps]) + len(cmaps)
    fig, axes = plt.subplots(nrows=nrows, figsize=(8, 6))
    fig.subplots_adjust(top=0.95, bottom=0.01, left=0.25, right=0.99)
    curr_ax = 0
    for cmap_category in cmaps:
        cmap_list = cmaps[cmap_category]
        axes[curr_ax + 1].set_title(cmap_category + ' colormaps', fontsize=12)
        curr_ax += 1
        for cmap in cmap_list:
            ax = axes[curr_ax]
            ax.imshow(gradient, aspect='auto', cmap=cmap)
            pos = list(ax.get_position().bounds)
            x_text = pos[0] - 0.01
            y_text = pos[1] + pos[3] / 2.
            name = parse_name(cmap)
            fig.text(x_text, y_text, name,
                     va='center', ha='right', fontsize=10)
            curr_ax += 1

    for ax in axes:
        ax.set_axis_off()


plot_color_gradients(cmaps)

os.remove("quantcmaps.py")
for cmap_category in cmaps:
    cmap_list = cmaps[cmap_category]
    for cmap in cmap_list:
        name = parse_name(cmap)
        save_to_py(cmap, name, "quantcmaps.py")

plt.savefig("quant_cmaps.png", dpi=300)
