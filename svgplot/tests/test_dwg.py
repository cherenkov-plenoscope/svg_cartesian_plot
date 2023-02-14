import svgwrite
import numpy as np


def Dwg(cols=1600, rows=900):
    dwg = svgwrite.Drawing(
        profile="full", size=("{:d}px".format(cols), "{:d}px".format(rows)),
    )
    dwg.viewbox(minx=0, miny=-rows, width=cols, height=rows)
    return dwg


def _shape(xy):
    try:
        _ = len(xy[0])
        return "list_of_points"
    except TypeError as e:
        return "point"


def _cartesian2bullshit(xy):
    shape = _shape(xy)
    if shape == "list_of_points":
        return [(p[0], -1.0 * p[1]) for p in xy]
    elif shape == "point":
        return (xy[0], -1.0 * xy[1])
    else:
        raise AssertionError("bad shape")


def Path(xy, **kwargs):
    pa = svgwrite.path.Path(**kwargs)
    pa.push("M")
    for p in xy:
        dwg_p = _cartesian2bullshit(p)
        pa.push("{:e},{:e}".format(dwg_p[0], dwg_p[1]))
    return pa


def Text(xy=[0, 0], r=0.0, **kwargs):
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


def _transform_point(xy, t, r):
    phi = np.deg2rad(r)
    ox = np.cos(phi) * xy[0] - np.sin(phi) * xy[1] + t[0]
    oy = np.sin(phi) * xy[0] + np.cos(phi) * xy[1] + t[1]
    return [ox, oy]


def transform(xy, t, r):
    """
    Parameters
    ----------
    xy : list / tuple, or list of lists / tuples
        The coordinates to be transformed.
    t : list / tuple
        Translation-vector.
    r : float
        Rotation angle in degrees.
    """
    shape = _shape(xy)
    if shape == "list_of_points":
        return [_transform_point(xy=p, t=t, r=r) for p in xy]
    elif shape == "point":
        return transform_point(xy=xy, t=t, r=r)
    else:
        raise AssertionError("bad shape")


dwg = Dwg(cols=1280, rows=720)
dwg.add(
    Path(
        xy=transform(xy=[[0, 0], [1280, 0]], t=[100, 200], r=15.0),
        id="hans",
        stroke="red",
        stroke_width=5,
    )
)
dwg.add(
    Path(xy=[[0, 0], [1280, 720]], id="hans", stroke="blue", stroke_width=5)
)
dwg.add(Path(xy=[[0, 0], [0, 720]], id="hans", stroke="green", stroke_width=5))
dwg.add(Text(xy=[100, 200], r=15, text="AbC"))
write(dwg, "mydwg.svg")
