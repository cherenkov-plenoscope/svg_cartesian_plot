def scientific(
    real,
    format_template="{:e}",
    nan_template="nan",
    drop_mantisse_if_one=True,
):
    if real != real:
        return nan_template
    assert format_template.endswith("e}")
    s = format_template.format(real)

    pos_e = s.find("e")
    assert pos_e >= 0
    mantisse = s[0:pos_e]
    exponent = str(int(s[pos_e + 1 :]))
    ten_to_power = "10" + superscript(exponent)
    if drop_mantisse_if_one and float(mantisse) == 1.0:
        out = ten_to_power
    else:
        out = mantisse + dot() + ten_to_power
    return out


def superscript(v):
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
    out = ""
    for c in v:
        out += m[v]
    return out


def dot():
    return "\u00B7"


def circ():
    return "\u00B0"
