import numpy as np
from . import svgcartesian
from . import scaling
from . import image


def Fig(cols=1920, rows=1080):
    f = {}
    f["fig"] = {}
    f["fig"]["cols"] = cols
    f["fig"]["rows"] = rows
    f["axes"] = []
    f["dwg"] = svgcartesian.Dwg(cols=f["fig"]["cols"], rows=f["fig"]["rows"])
    f["path_id_counter"] = 0
    return f


def Ax(fig):
    a = {}
    a["fig"] = fig
    a["span"] = (0.1, 0.1, 0.8, 0.8)
    a["xlim"] = (0, 1)
    a["ylim"] = (0, 1)
    a["xscale"] = scaling.unity()
    a["yscale"] = scaling.unity()
    fig["axes"].append(a)
    return a


def _ax2dwg_point(xy, fig, ax):
    x = ax["xscale"](xy[0])
    y = ax["yscale"](xy[1])

    xlim0 = ax["xscale"](ax["xlim"][0])
    xlim1 = ax["xscale"](ax["xlim"][1])

    ylim0 = ax["yscale"](ax["ylim"][0])
    ylim1 = ax["yscale"](ax["ylim"][1])

    x_range = xlim1 - xlim0
    x_ax_rel = (x - xlim0) / x_range

    x_ax_range = ax["span"][2]
    x_fig_rel = ax["span"][0] + x_ax_range * x_ax_rel
    x_fig = x_fig_rel * fig["fig"]["cols"]

    y_range = ylim1 - ylim0
    y_ax_rel = (y - ylim0) / y_range

    y_ax_range = ax["span"][3]
    y_fig_rel = ax["span"][1] + y_ax_range * y_ax_rel
    y_fig = y_fig_rel * fig["fig"]["rows"]

    return x_fig, y_fig


def _ax2dwg(xy, fig, ax):
    shape = svgcartesian._shape(xy)
    if shape == "point":
        return _ax2dwg_point(xy=xy, fig=fig, ax=ax)
    elif shape == "list_of_points":
        return [_ax2dwg_point(xy=p, fig=fig, ax=ax) for p in xy]
    else:
        raise AssertionError("bad shape")


def ax_add_line(ax, xy_start, xy_stop, **kwargs):
    dwg = ax["fig"]["dwg"]
    fig = ax["fig"]
    dwg.add(
        svgcartesian.Line(
            xy_start=_ax2dwg(xy_start, fig=fig, ax=ax),
            xy_stop=_ax2dwg(xy_stop, fig=fig, ax=ax),
            **kwargs,
        )
    )


def ax_add_path(ax, xy, **kwargs):
    dwg = ax["fig"]["dwg"]
    fig = ax["fig"]

    dwg.add(svgcartesian.Path(xy=_ax2dwg(xy, fig=fig, ax=ax), **kwargs))


def ax_add_text(ax, xy=[0, 0], r=0.0, **kwargs):
    dwg = ax["fig"]["dwg"]
    fig = ax["fig"]
    dwg.add(svgcartesian.Text(xy=_ax2dwg(xy, fig=fig, ax=ax), r=r, **kwargs))


def fig_write(fig, path):
    dwg = fig["dwg"]
    svgcartesian.write(dwg=fig["dwg"], path=path)


def ax_add_pcolormesh(ax, z, colormap, x_bin_edges=None, y_bin_edges=None, **kwargs):

    """
        (x0, y1)     (x1, y1)
            +-----------+
            |           |
            |           |
            |           |
            |           |
            +-----------+
        (x0, y0)     (x1, y0)
    """

    z = np.asarray(z)
    num_x = z.shape[0]
    num_y = z.shape[1]

    if x_bin_edges is None:
        x_bin_edges = np.arange(0, num_x + 1)

    if y_bin_edges is None:
        y_bin_edges = np.arange(0, num_y + 1)

    mat = np.zeros(shape=(num_x, num_y, 3), dtype=np.uint8)

    for xbin in range(num_x):
        for ybin in range(num_y):
            mat[xbin, num_y - ybin - 1] = colormap(z[xbin, ybin])

    mat64_str = image.image_to_png_base64(mat=mat)

    fig = ax["fig"]
    dwg = fig["dwg"]

    start_xy = _ax2dwg([0, 0], fig=fig, ax=ax)
    stop_xy = _ax2dwg([1, 1], fig=fig, ax=ax)

    range_x = stop_xy[0] - start_xy[0]
    range_y = stop_xy[1] - start_xy[1]

    dwg.add(
        dwg.image(
            href="data:image/png;base64," + mat64_str,
            width="{:f}".format(range_x),
            height="{:f}".format(range_y),
            x="{:f}".format(start_xy[0]),
            y="{:f}".format(start_xy[1] - fig["fig"]["rows"]),
        )
    )
