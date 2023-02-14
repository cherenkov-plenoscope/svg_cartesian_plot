from . import base as splt
import numpy as np


EXAMPLE_MIRROR_CONFIG = {
    "focal_length": 1.0,
    "diameter": 0.8,
    "deformation": {"amplitude": 0.0, "phase": 0.0},
}


def ax_add_optical_axis(
    ax,
    mirror_diameter,
    mirror_focal_length,
    sensor_diameter,
    overhead=1.05,
    **kwargs,
):
    mD = mirror_diameter
    mF = mirror_focal_length
    sD = sensor_diameter
    oH = overhead

    splt.ax_add_line(
        ax=ax, xy_start=(0, -mF * 0.5 * (oH - 1)), xy_stop=(0, mF * 1.1 * oH), **kwargs
    )
    splt.ax_add_line(
        ax=ax, xy_start=(-oH * mD / 2, 0.0), xy_stop=(oH * mD / 2, 0.0), **kwargs
    )
    splt.ax_add_line(
        ax=ax, xy_start=(-oH * sD / 2, mF), xy_stop=(oH * sD / 2, mF), **kwargs
    )


def make_mirror_points(
    mirror_config, x_range=None, fn=101,
):
    mD = mirror_config["diameter"]
    mF = mirror_config["focal_length"]

    if x_range == None:
        x_range = [-mD / 2, mD / 2]

    mirror_points = []
    for x in np.linspace(x_range[0], x_range[1], fn):
        y = (x ** 2) / (4.0 * mF)

        xrel = x / (mD / 2) + mirror_config["deformation"]["phase"]
        y_def = np.sin(x * 2 * np.pi) * mirror_config["deformation"]["amplitude"]

        mirror_points.append([x, y + y_def])
    return mirror_points


def ax_add_mirror(
    ax, mirror_config, **kwargs,
):
    mirror_points = make_mirror_points(mirror_config,)
    splt.ax_add_path(ax=ax, xy=mirror_points, **kwargs)


def _light_field_sensor_photo_sensor_x(
    img_x, mirror_x, mirror_diameter,
):
    lens_diameter = img_x[1] - img_x[0]

    x_start = img_x[0] + lens_diameter / 2
    x_stop = img_x[0] + lens_diameter / 2

    x_stop += -(lens_diameter / mirror_diameter * mirror_x[0])
    x_start += -(lens_diameter / mirror_diameter * mirror_x[1])
    return (x_start, x_stop)


EXAMPLE_SENSOR_CONFIG = {
    "diameter": EXAMPLE_MIRROR_CONFIG["diameter"] / 1.5,
    "translation": [0.0, EXAMPLE_MIRROR_CONFIG["focal_length"]],
    "rotation": 0.0,
    "num_pixel": 5,
    "num_paxel": 5,
}


def _light_field_sensor_photo_sensor_distance(
    mirror_focal_length, mirror_diameter, img_x, img_distance,
):
    F_STOP_RATIO = mirror_focal_length / mirror_diameter
    lens_diameter = img_x[1] - img_x[0]
    lens_focal_length = lens_diameter * F_STOP_RATIO

    return img_distance + lens_focal_length


def ax_add_beam(
    ax,
    img_x,
    img_distance,
    beam_distance,
    mirror_x,
    mirror_config,
    show_beam_scenery_to_mirror=True,
    show_beam_mirror_to_sensor_plane=True,
    show_beam_lens_to_photo_sensor=True,
    **kwargs,
):
    mF = mirror_config["focal_length"]

    if show_beam_mirror_to_sensor_plane:
        img_x_start = img_x[0]
        img_x_stop = img_x[1]

        mirror_points = make_mirror_points(
            x_range=mirror_x,
            mirror_config=mirror_config,
        )

        img_beam_points = []
        img_beam_points.append([img_x_stop, img_distance])
        img_beam_points.append([img_x_start, img_distance])
        img_beam_points += list(mirror_points)

        splt.ax_add_path(
            ax=ax, xy=img_beam_points, **kwargs,
        )

    if show_beam_scenery_to_mirror:
        img_x_start_at_focal_length = img_x_start * (mF / img_distance)
        img_x_stop_at_focal_length = img_x_stop * (mF / img_distance)

        beam_x_start_at_focal_length = -img_x_stop_at_focal_length
        beam_x_stop_at_focal_length = -img_x_start_at_focal_length

        """
        beam_points = []
        beam_points.append([beam_x_stop_at_focal_length + mirror_x[1], mF])
        beam_points.append([beam_x_start_at_focal_length + mirror_x[0], mF])
        beam_points += list(mirror_points)

        splt.ax_add_path(
            ax=ax,
            points=beam_points,
            stroke_color=stroke_color,
            stroke_width=stroke_width,
            alpha=alpha,
            fill_color=(0,255,0),
        )
        """

        beam_x_start_at_beam_distance = (
            beam_x_start_at_focal_length / mF * beam_distance
        )
        beam_x_stop_at_beam_distance = (
            beam_x_stop_at_focal_length / mF * beam_distance
        )

        beam_points = []
        beam_points.append(
            [beam_x_stop_at_beam_distance + mirror_x[1], beam_distance]
        )
        beam_points.append(
            [beam_x_start_at_beam_distance + mirror_x[0], beam_distance]
        )
        beam_points += list(mirror_points)

        splt.ax_add_path(
            ax=ax, xy=beam_points, **kwargs,
        )

    # beam from lens to sensor
    # ------------------------
    if show_beam_lens_to_photo_sensor:
        lsbeam_points = []
        lsbeam_points.append((img_x_start, img_distance))
        lsbeam_points.append((img_x_stop, img_distance))

        light_field_sensor_photo_sensor_distance = _light_field_sensor_photo_sensor_distance(
            mirror_focal_length=mirror_config["focal_length"],
            mirror_diameter=mirror_config["diameter"],
            img_x=img_x,
            img_distance=img_distance,
        )

        (
            photo_sensor_x_start,
            photo_sensor_x_stop,
        ) = _light_field_sensor_photo_sensor_x(
            img_x=img_x, mirror_x=mirror_x, mirror_diameter=mirror_config["diameter"],
        )

        lsbeam_points.append(
            (photo_sensor_x_stop, light_field_sensor_photo_sensor_distance)
        )
        lsbeam_points.append(
            (photo_sensor_x_start, light_field_sensor_photo_sensor_distance)
        )

        splt.ax_add_path(
            ax=ax, xy=lsbeam_points, **kwargs,
        )


def ax_add_lens(
    ax, img_x, img_distance, fn=25, **kwargs,
):
    x_r = (img_x[1] - img_x[0]) / 2
    lens_points = []
    _y_max = (x_r ** 2) / (4.0 * x_r)

    # lower bow
    for _x in np.linspace(-x_r, x_r, fn):
        _y = (_x ** 2) / (4.0 * x_r)

        x = _x + img_x[0] + x_r
        y = _y + img_distance - _y_max

        lens_points.append([x, y])

    # upper bow
    for _x in np.linspace(x_r, -x_r, fn):
        _y = -1.0 * (_x ** 2) / (4.0 * x_r)

        x = _x + img_x[0] + x_r
        y = _y + img_distance + _y_max

        lens_points.append([x, y])

    splt.ax_add_path(
        ax=ax, xy=lens_points, **kwargs,
    )


def ax_add_lens_seperator_walls(
    ax, img_x, img_distance, mirror_diameter, mirror_focal_length, **kwargs,
):
    lfs_photo_sensor_distance = _light_field_sensor_photo_sensor_distance(
        mirror_focal_length=mirror_focal_length,
        mirror_diameter=mirror_diameter,
        img_x=img_x,
        img_distance=img_distance,
    )

    for l in [0, 1]:
        splt.ax_add_line(
            ax=ax,
            xy_start=[img_x[l], lfs_photo_sensor_distance],
            xy_stop=[img_x[l], img_distance],
            **kwargs,
        )


def make_photo_sensor_xy(width, height):
    x = width / 2
    w = width
    h = height
    points = []
    points.append((-x, 0))
    points.append((x, 0))
    points.append((x - 0.25 * w, h * 0.33))
    points.append((x - 0.25 * w, h))
    points.append((-x + 0.25 * w, h))
    points.append((-x + 0.25 * w, h * 0.33))
    return points


def ax_add_photo_sensor(ax, T, width, height):
    xy = make_photo_sensor_xy(width=width, height=height)
    xy = svgcartesian.transform(xy=xy, T=T)
    splt.ax_add_path(
        ax=ax, xy=points, **kwargs,
    )


def ax_add_image_sensor_photo_sensor(
    ax, img_x, img_distance, photo_sensor_height, **kwargs,
):
    img_w = img_x[1] - img_x[0]
    img_d = img_distance
    phsh = photo_sensor_height

    points = []
    points.append((img_x[0], img_d))
    points.append((img_x[1], img_d))
    points.append((img_x[1] - 0.25 * img_w, img_d + phsh * 0.33))
    points.append((img_x[1] - 0.25 * img_w, img_d + phsh))
    points.append((img_x[0] + 0.25 * img_w, img_d + phsh))
    points.append((img_x[0] + 0.25 * img_w, img_d + phsh * 0.33))

    splt.ax_add_path(
        ax=ax, xy=points, **kwargs,
    )


def ax_add_light_field_sensor_photo_sensor(
    ax,
    img_x,
    img_distance,
    photo_sensor_height,
    mirror_x,
    mirror_diameter,
    mirror_focal_length,
    **kwargs,
):
    phs_x = _light_field_sensor_photo_sensor_x(
        img_x=img_x, mirror_x=mirror_x, mirror_diameter=mirror_diameter,
    )

    lfs_photo_sensor_distance = _light_field_sensor_photo_sensor_distance(
        mirror_focal_length=mirror_focal_length,
        mirror_diameter=mirror_diameter,
        img_x=img_x,
        img_distance=img_distance,
    )

    lfs_d = lfs_photo_sensor_distance
    phs_w = phs_x[1] - phs_x[0]
    phsh = photo_sensor_height

    points = []
    points.append((phs_x[0], lfs_d))
    points.append((phs_x[1], lfs_d))
    points.append((phs_x[1] - 0.25 * phs_w, lfs_d + phsh * 0.33))
    points.append((phs_x[1] - 0.25 * phs_w, lfs_d + phsh))
    points.append((phs_x[0] + 0.25 * phs_w, lfs_d + phsh))
    points.append((phs_x[0] + 0.25 * phs_w, lfs_d + phsh * 0.33))

    splt.ax_add_path(
        ax=ax, xy=points, **kwargs,
    )


def make_bin_start_stops(diameter, num_bins):
    sD = diameter
    bin_pos = []
    bin_w = sD / num_bins
    for bin_x_start in np.linspace(-sD / 2, sD / 2, num_bins, endpoint=False):
        bin_pos.append((bin_x_start, bin_x_start + bin_w))
    return bin_pos
