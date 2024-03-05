from . import colormap_storage
from .. import base
from .. import scaling
import numpy as np


class Map:
    def __init__(self, name, start=0.0, stop=1.0, func=scaling.unity()):
        assert start < stop
        self.name = name
        self.start = start
        self.stop = stop
        self.func = func
        self.rgb = getattr(colormap_storage, name)()
        self.vals = np.linspace(0.0, 1.0, len(self.rgb))

    def __call__(self, val):
        return self.eval(val=val)

    def eval(self, val):
        _val = self.func(val)
        _start = self.func(self.start)
        _stop = self.func(self.stop)
        val1 = _compress_zero_to_one(x=_val, x_start=_start, x_stop=_stop)

        rgb_out = np.zeros(3)
        for c in range(3):
            rgb_out[c] = np.interp(
                x=val1,
                xp=self.vals,
                fp=self.rgb[:, c],
            )

        rgb8 = (255 * rgb_out).astype(np.uint8)
        return (int(rgb8[0]), int(rgb8[1]), int(rgb8[2]))

    def __repr__(self):
        out = "{:s}(name={:s}, start={:f}, stop={:f}, func={:s})".format(
            self.__class__.__name__,
            self.name,
            self.start,
            self.stop,
            self.func.__name__,
        )
        return out


def ax_add_colormap(ax, colormap, fn=51, orientation="horizontal"):
    scale = ax["yscale"]
    ds = np.linspace(
        scale(colormap.start),
        scale(colormap.stop),
        fn + 1,
    )
    ds = scale.inverse(ds)

    dd = ds[1:] - ds[:-1]

    if orientation == "horizontal":
        ax["xlim"] = [colormap.start, colormap.stop]
        ax["ylim"] = [0.0, 1.0]
        for i in range(fn):
            rect_xy = _rectangle_path(xy=[ds[i], 0.0], dx=dd[i], dy=1.0)
            d_mean = 0.5 * (ds[i] + ds[i + 1])
            _color = colormap(d_mean)
            base.ax_add_path(ax=ax, xy=rect_xy, fill=_color, stroke=_color)
    elif orientation == "vertical":
        ax["ylim"] = [colormap.start, colormap.stop]
        ax["xlim"] = [0.0, 1.0]
        for i in range(fn):
            rect_xy = _rectangle_path(xy=[0.0, ds[i]], dx=1.0, dy=dd[i])
            d_mean = 0.5 * (ds[i] + ds[i + 1])
            _color = colormap(d_mean)
            base.ax_add_path(ax=ax, xy=rect_xy, fill=_color, stroke=_color)
    else:
        raise ValueError("No such orientation '{:s}'.".format(orientation))


def ax_add_colormap_ticks(
    ax, colormap, num, orientation="horizontal", **kwargs
):
    if orientation == "horizontal":
        raise NotImplementedError("Oops")
    elif orientation == "vertical":
        if isinstance(ax["yscale"], scaling.unity):
            tick_values = list_ticks_in_range_linear(
                start=colormap.start, stop=colormap.stop
            )
            fmt = "{:.1f}"
            tick_labels = []
            for i in range(len(tick_values)):
                tick_labels.append(fmt.format(tick_values[i]))
        else:
            tick_values = list_ticks_in_range_log(
                start=colormap.start, stop=colormap.stop
            )
            tick_values = tick_values.astype(float)
            if len(tick_values) > num:
                keep = np.arange(0, len(tick_values), len(tick_values) // num)
                tick_values = tick_values[keep]
            tick_labels = []
            for i in range(len(tick_values)):
                tick_labels.append(
                    utf8_scientific(
                        real=tick_values[i], format_template="{:.2e}"
                    )
                )

        for i in range(len(tick_values)):
            base.ax_add_text(
                ax=ax, xy=[1.1, tick_values[i]], text=tick_labels[i], **kwargs
            )

    else:
        raise ValueError("No such orientation '{:s}'.".format(orientation))


def _rectangle_path(xy, dx, dy):
    x = xy[0]
    y = xy[1]
    verts = [
        (x, y),
        (x + dx, y),
        (x + dx, y + dy),
        (x, y + dy),
    ]
    return verts


def _compress_zero_to_one(x, x_start, x_stop):
    if x >= x_stop:
        return 1
    elif x < x_start:
        return 0
    return (x - x_start) / (x_stop - x_start)


def css(s):
    s = str.lower(s)
    d = {
        "aliceblue": (240, 248, 255),
        "antiquewhite": (250, 235, 215),
        "aqua": (0, 255, 255),
        "aquamarine": (127, 255, 212),
        "azure": (240, 255, 255),
        "beige": (245, 245, 220),
        "bisque": (255, 228, 196),
        "black": (0, 0, 0),
        "blanchedalmond": (255, 255, 205),
        "blue": (0, 0, 255),
        "blueviolet": (138, 43, 226),
        "brown": (165, 42, 42),
        "burlywood": (222, 184, 135),
        "cadetblue": (95, 158, 160),
        "chartreuse": (127, 255, 0),
        "chocolate": (210, 105, 30),
        "coral": (255, 127, 80),
        "cornflowerblue": (100, 149, 237),
        "cornsilk": (255, 248, 220),
        "crimson": (220, 20, 60),
        "cyan": (0, 255, 255),
        "darkblue": (0, 0, 139),
        "darkcyan": (0, 139, 139),
        "darkgoldenrod": (184, 134, 11),
        "darkgray": (169, 169, 169),
        "darkgreen": (0, 100, 0),
        "darkkhaki": (189, 183, 107),
        "darkmagenta": (139, 0, 139),
        "darkolivegreen": (85, 107, 47),
        "darkorange": (255, 140, 0),
        "darkorchid": (153, 50, 204),
        "darkred": (139, 0, 0),
        "darksalmon": (233, 150, 122),
        "darkseagreen": (143, 188, 143),
        "darkslateblue": (72, 61, 139),
        "darkslategray": (47, 79, 79),
        "darkturquoise": (0, 206, 209),
        "darkviolet": (148, 0, 211),
        "deeppink": (255, 20, 147),
        "deepskyblue": (0, 191, 255),
        "dimgray": (105, 105, 105),
        "dodgerblue": (30, 144, 255),
        "firebrick": (178, 34, 34),
        "floralwhite": (255, 250, 240),
        "forestgreen": (34, 139, 34),
        "fuchsia": (255, 0, 255),
        "gainsboro": (220, 220, 220),
        "ghostwhite": (248, 248, 255),
        "gold": (255, 215, 0),
        "goldenrod": (218, 165, 32),
        "gray": (128, 128, 128),
        "green": (0, 128, 0),
        "greenyellow": (173, 255, 47),
        "honeydew": (240, 255, 240),
        "hotpink": (255, 105, 180),
        "indianred": (205, 92, 92),
        "indigo": (75, 0, 130),
        "khaki": (240, 230, 140),
        "lavender": (230, 230, 250),
        "lavenderblush": (255, 240, 245),
        "lawngreen": (124, 252, 0),
        "lemonchiffon": (255, 250, 205),
        "lightblue": (173, 216, 230),
        "lightcoral": (240, 128, 128),
        "lightcyan": (224, 255, 255),
        "lightgoldenrod-yellow": (250, 250, 210),
        "lightgreen": (144, 238, 144),
        "lightgrey": (211, 211, 211),
        "lightpink": (255, 182, 193),
        "lightsalmon": (255, 160, 122),
        "lightseagreen": (32, 178, 170),
        "lightskyblue": (135, 206, 250),
        "lightslategray": (119, 136, 153),
        "lightsteelblue": (176, 196, 222),
        "lightyellow": (255, 255, 224),
        "lime": (0, 255, 0),
        "limegreen": (50, 205, 50),
        "linen": (250, 240, 230),
        "magenta": (255, 0, 255),
        "maroon": (128, 0, 0),
        "mediumaquamarine": (102, 205, 170),
        "mediumblue": (0, 0, 205),
        "mediumorchid": (186, 85, 211),
        "mediumpurple": (147, 112, 219),
        "mediumseagreen": (60, 179, 113),
        "mediumslateblue": (123, 104, 238),
        "mediumspringgreen": (0, 250, 154),
        "mediumturquoise": (72, 209, 204),
        "mediumvioletred": (199, 21, 133),
        "midnightblue": (25, 25, 112),
        "mintcream": (245, 255, 250),
        "mistyrose": (55, 228, 225),
        "moccasin": (255, 228, 181),
        "navajowhite": (255, 222, 173),
        "navy": (0, 0, 128),
        "oldlace": (253, 245, 230),
        "olive": (128, 128, 0),
        "olivedrab": (107, 142, 35),
        "orange": (255, 165, 0),
        "orangered": (255, 69, 0),
        "orchid": (218, 112, 214),
        "palegoldenrod": (238, 232, 170),
        "palegreen": (152, 251, 152),
        "paleturquoise": (75, 238, 238),
        "palevioletred": (219, 112, 147),
        "papayawhip": (255, 239, 213),
        "peachpuff": (255, 239, 213),
        "peru": (205, 133, 63),
        "pink": (255, 192, 203),
        "plum": (221, 160, 221),
        "powderblue": (176, 224, 230),
        "purple": (128, 0, 128),
        "rebeccapurple": (102, 51, 153),
        "red": (225, 0, 0),
        "rosybrown": (188, 143, 143),
        "royalblue": (65, 105, 225),
        "saddlebrown": (139, 69, 19),
        "salmon": (250, 128, 114),
        "sandybrown": (44, 164, 96),
        "seagreen": (46, 139, 87),
        "seashell": (255, 245, 238),
        "sienna": (160, 82, 45),
        "silver": (192, 192, 192),
        "skyblue": (135, 206, 235),
        "slateblue": (106, 90, 205),
        "slategray": (112, 128, 144),
        "snow": (255, 250, 250),
        "springgreen": (0, 255, 127),
        "steelblue": (70, 130, 180),
        "tan": (210, 180, 140),
        "teal": (0, 128, 128),
        "thistle": (216, 191, 216),
        "tomato": (253, 99, 71),
        "turquoise": (64, 224, 208),
        "violet": (238, 130, 238),
        "wheat": (245, 222, 179),
        "white": (255, 255, 255),
        "whitesmoke": (245, 245, 245),
        "yellow": (255, 255, 0),
        "yellowgreen": (154, 205, 50),
    }
    return d[s]


def next_lower_decade(x):
    return int(np.floor(np.log10(x)))


def next_higher_decade(x):
    return int(np.ceil(np.log10(x)))


def list_ticks_in_range_linear(start, stop, num=10):
    assert stop >= start
    span = stop - start
    step_decade = int(np.floor(np.log10(span)))

    dstart = np.round(start, -step_decade)
    dstop = np.round(stop, -step_decade)
    dstep = 10 ** (step_decade - 1)
    out = np.arange(dstart, dstop + dstep, dstep)

    while len(out) > num:
        dstep *= 2
        out = np.arange(dstart, dstop + dstep, dstep)

    return out


def list_ticks_in_range_log(start, stop):
    assert stop >= start
    lowest_inner_decade = next_higher_decade(start)
    highest_inner_decade = next_lower_decade(stop)
    dec_diff = highest_inner_decade - lowest_inner_decade
    a = 10**lowest_inner_decade
    b = 10**highest_inner_decade
    return np.geomspace(a, b, dec_diff + 1)


def utf8_scientific(
    real,
    format_template="{:e}",
    nan_template="nan",
    drop_mantisse_if_one=True,
):
    if real != real:
        return nan_template
    assert format_template.endswith("e}")
    s = format_template.format(real)

    mittelpunkt = "\u00B7"
    pos_e = s.find("e")
    assert pos_e >= 0
    mantisse = s[0:pos_e]
    exponent = str(int(s[pos_e + 1 :]))
    ten_to_power = "10" + str.join("", [hochgestellt(v) for v in exponent])
    if drop_mantisse_if_one and float(mantisse) == 1.0:
        out = ten_to_power
    else:
        out = mantisse + mittelpunkt + ten_to_power
    return out


def hochgestellt(v):
    m = {
        "-": "\u207B",
        "+": "\u207A",
        "0": "\u2070",
        "1": "\u00B9",
        "2": "\u00B2",
        "3": "\u00B3",
        "4": "\u2074",
        "5": "\u2075",
        "6": "\u2076",
        "7": "\u2077",
        "8": "\u2078",
        "9": "\u2079",
    }
    return m[v]


def circ():
    return "\u00B0"
