import matplotlib as mpl
import matplotlib.cm as cm
import io
import numpy as np

NN = 2**8
maps = {}

colormaps_without_reverse = []
for key in mpl.colormaps():
    if not "_r" in key:
        colormaps_without_reverse.append(key)

for key in colormaps_without_reverse:
    maps[key] = np.zeros(shape=(NN, 4))
    mm = getattr(cm, key)
    for i, v in enumerate(np.linspace(0, 1, NN)):
        maps[key][i] = np.array(mm(v))

o = io.StringIO()
o.write("import numpy as np")
o.write("\n")
o.write("\n")
o.write("def _hex_to_array(h):\n")
o.write("    arr = np.array(\n")
o.write(
    "        [int(h[i : i + 2], base=16) for i in np.arange(0, len(h), 2)]\n"
)
o.write("    )\n")
o.write("    return (1 / 255) * arr.reshape((len(arr) // 3, 3))\n")
o.write("\n")
o.write("\n")
for key in maps:
    rgb8 = maps[key] * (2**8 - 1)
    assert np.all(rgb8 >= 0.0)
    assert np.all(rgb8 < (2**8))
    rgb8 = rgb8.astype("u1")
    o.write("def {:s}():\n".format(key))
    o.write('    h = "')
    for i in range(NN):
        o.write(
            "{:02x}{:02x}{:02x}".format(rgb8[i][0], rgb8[i][1], rgb8[i][2])
        )
    o.write('"\n')
    o.write("    return _hex_to_array(h)\n")
    o.write("\n")
    o.write("\n")
o.seek(0)

with open("colormaps_adopted_from_matplotlib.py", "wt") as f:
    f.write(o.read())
