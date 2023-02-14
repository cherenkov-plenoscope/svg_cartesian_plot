import numpy as np
from . import svgcartesian


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
    fig["axes"].append(a)
    return a


def _ax2dwg_point(xy, fig, ax):
    x = xy[0]
    y = xy[1]
    x_range = ax["xlim"][1] - ax["xlim"][0]
    x_ax_rel = (x - ax["xlim"][0]) / x_range

    x_ax_range = ax["span"][2]
    x_fig_rel = ax["span"][0] + x_ax_range * x_ax_rel
    x_fig = x_fig_rel * fig["fig"]["cols"]

    y_range = ax["ylim"][1] - ax["ylim"][0]
    y_ax_rel = (y - ax["ylim"][0]) / y_range

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
            **kwargs
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
