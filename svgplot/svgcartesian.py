import svgwrite
import numpy as np
import os
import subprocess
import tempfile


def Dwg(cols=1600, rows=900):
    dwg = svgwrite.Drawing(
        profile="full", size=("{:d}px".format(cols), "{:d}px".format(rows)),
    )
    dwg.viewbox(minx=0, miny=-rows, width=cols, height=rows)
    return dwg


def _shape(xy):
    """
    Determine the shape of the xy coordinates
    """
    try:
        _ = len(xy[0])
        return "list_of_points"
    except TypeError as e:
        return "point"


def _cartesian2bullshit(xy):
    """
    Flip the y-axis. Stupid SVG.
    """
    shape = _shape(xy)
    if shape == "list_of_points":
        return [(p[0], -1.0 * p[1]) for p in xy]
    elif shape == "point":
        return (xy[0], -1.0 * xy[1])
    else:
        raise AssertionError("bad shape")


def Path(xy, **kwargs):
    kwargs = color_replacer(**kwargs)

    pa = svgwrite.path.Path(**kwargs)
    pa.push("M")
    for p in xy:
        dwg_p = _cartesian2bullshit(p)
        pa.push("{:e},{:e}".format(dwg_p[0], dwg_p[1]))
    return pa


def Line(xy_start, xy_stop, **kwargs):
    kwargs = color_replacer(**kwargs)

    return svgwrite.shapes.Line(
        _cartesian2bullshit(xy_start), _cartesian2bullshit(xy_stop), **kwargs
    )


def Text(xy=[0, 0], r=0.0, **kwargs):
    kwargs = color_replacer(**kwargs)

    _t = _cartesian2bullshit(xy)
    return svgwrite.text.Text(
        insert=[0, 0],
        transform="translate({:f} {:f}) rotate({:f})".format(_t[0], _t[1], -r),
        **kwargs,
    )


def write(dwg, path):
    if str.endswith(str.lower(path), ".jpg"):
        dwg_filename = str(dwg.filename)
        with tempfile.TemporaryDirectory() as tmpdir:
            dwg.filename = os.path.join(tmpdir, "my.svg")
            dwg.save(pretty=True, indent=4)
            subprocess.call(["convert", dwg.filename, path])
        dwg.filename = dwg_filename

    elif str.endswith(str.lower(path), ".svg"):
        dwg_filename = str(dwg.filename)
        dwg.filename = path
        dwg.save(pretty=True, indent=4)
        dwg.filename = dwg_filename

    else:
        raise AssertionError("unknown format")


def _transform_point(xy, T):
    phi = np.deg2rad(r)
    ox = T[0, 0] * xy[0] + T[0, 1] * xy[1] + T[0, 2]
    oy = T[1, 0] * xy[0] + T[1, 1] * xy[1] + T[1, 2]
    return [ox, oy]


def transform(xy, T):
    """
    Parameters
    ----------
    xy : list / tuple, or list of lists / tuples
        The coordinates to be transformed.
    T : matrix
        Homogeneous transformation matrix.
    """
    shape = _shape(xy)
    if shape == "list_of_points":
        return [_transform_point(xy=p, T=T) for p in xy]
    elif shape == "point":
        return transform_point(xy=xy, T=T)
    else:
        raise AssertionError("bad shape")


def Rotation(phi):
    return [
        [np.cos(phi), -np.sin(phi), 0.0],
        [np.sin(phi), np.cos(phi), 0.0],
        [0, 0, 1],
    ]


def Translation(xy):
    return [
        [1, 0, xy[0]],
        [0, 1, xy[1]],
        [0, 0, 1],
    ]


def concatenate(A, B):
    return [
        [A[0, 0] * B[0, 0] + A[0, 1] * B[1, 0] + A[0, 2] * B[2, 0]],
        [A[1, 0] * B[0, 1] + A[1, 1] * B[1, 1] + A[1, 2] * B[2, 1]],
        [A[2, 0] * B[0, 2] + A[2, 1] * B[1, 2] + A[2, 2] * B[2, 2]],
    ]


def color255(rgb=None):
    if rgb == None:
        return "none"
    if len(rgb) == 3:
        assert rgb[0] <= 255
        assert rgb[1] <= 255
        assert rgb[2] <= 255
        return (
            "#"
            + "{0:02X}".format(rgb[0])
            + "{0:02X}".format(rgb[1])
            + "{0:02X}".format(rgb[2])
        )
    raise AssertionError("unknown color format")


def color_replacer(**kwargs):
    if "fill" in kwargs:
        kwargs["fill"] = color255(kwargs["fill"])
    if "stroke" in kwargs:
        kwargs["stroke"] = color255(kwargs["stroke"])
    return kwargs
