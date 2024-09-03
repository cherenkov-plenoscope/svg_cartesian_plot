import svg_cartesian_plot as splt
import numpy as np

DARKMODE = True

COLOR_SENSOR = (192, 0, 0)
COLOR_BEAM = (0, 128, 255)
COLOR_WALLS = (0, 192, 0)

if DARKMODE:
    STROKE = (255, 255, 255)
    EXT = ".dark"
    BEAM_OPACITY = 0.5
    COLOR_LENS = (100, 200, 255)
else:
    STROKE = (0, 0, 0)
    EXT = ""
    BEAM_OPACITY = 0.2
    COLOR_LENS = (50, 100, 255)

FIG_RATIO = 1.0
FIG_NUM_COLS = 1280

MIRROR = {
    "focal_length": 1.0,
    "diameter": 0.75,
    "deformation": {"amplitude": 0.0, "phase": 0.0},
}

IMG_DISTANCE = 1.0 * MIRROR["focal_length"]

SENSOR = {
    "diameter": MIRROR["diameter"] / 1.5,
    "translation": [0.0, MIRROR["focal_length"]],
    "rotation": 0.0,
    "num_pixel": 5,
    "num_paxel": 5,
}

AXSPAN = (0, 0, 1, 1)
AX_XLIM = (-0.75, 0.75)
AX_YLIM = (-0.05, 1.45)


def ax_add_scope(
    mirror,
    sensor,
    pixels,
    paxels,
):
    mD = mirror["diameter"]
    mF = mirror["focal_length"]
    sD = sensor["diameter"]
    img_d = sensor["translation"][1]

    ePixels = splt.optics.make_bin_start_stops(
        diameter=sD, num_bins=sensor["num_pixel"]
    )

    if sensor["num_paxel"] == 1:
        show_lenses = False
        paxels = [0]
        ePaxels = splt.optics.make_bin_start_stops(
            diameter=mD, num_bins=sensor["num_paxel"]
        )
    else:
        show_lenses = True
        ePaxels = splt.optics.make_bin_start_stops(
            diameter=mD, num_bins=sensor["num_paxel"]
        )

    for iPixel, tPixel in enumerate(ePixels):
        for iPaxel, tPaxel in enumerate(ePaxels):
            if iPixel in pixels and iPaxel in paxels:
                splt.optics.ax_add_beam(
                    ax=ax,
                    img_x=tPixel,
                    img_distance=img_d,
                    beam_distance=mF * 12,
                    mirror_x=tPaxel,
                    mirror_config=mirror,
                    fill=COLOR_BEAM,
                    fill_opacity=BEAM_OPACITY,
                    show_beam_scenery_to_mirror=True,
                    show_beam_mirror_to_sensor_plane=True,
                    show_beam_lens_to_photosensor=show_lenses,
                )

    for tPixel in ePixels:
        for tPaxel in ePaxels:
            if show_lenses:
                splt.optics.ax_add_light_field_sensor_photosensor(
                    ax=ax,
                    img_x=tPixel,
                    img_distance=img_d,
                    photosensor_height=mF * 0.05,
                    mirror_x=tPaxel,
                    mirror_diameter=mD,
                    mirror_focal_length=mF,
                    fill=COLOR_SENSOR,
                    fill_opacity=1.0,
                )

    for tPixel in ePixels:
        if show_lenses:
            splt.optics.ax_add_lens_seperator_walls(
                ax=ax,
                img_x=tPixel,
                img_distance=img_d,
                mirror_diameter=mD,
                mirror_focal_length=mF,
                stroke=COLOR_WALLS,
                stroke_width=5,
                stroke_opacity=1.0,
            )
            splt.optics.ax_add_lens(
                ax=ax,
                img_x=tPixel,
                img_distance=img_d,
                fill=COLOR_LENS,
                fill_opacity=0.5,
                stroke=STROKE,
                stroke_width=2.5,
                stroke_opacity=1.0,
            )
        else:
            splt.optics.ax_add_image_sensor_photosensor(
                ax=ax,
                img_x=tPixel,
                img_distance=img_d,
                photosensor_height=mF * 0.05,
                fill=COLOR_SENSOR,
                fill_opacity=1.0,
                stroke=STROKE,
            )

    splt.optics.ax_add_mirror(
        ax=ax,
        mirror_config=MIRROR,
        stroke_width=10,
        stroke=STROKE,
        fill=None,
    )


DEFORMATIONS = {
    "default": 0.0,
    "perlin55mm": MIRROR["focal_length"] * 0.01,
}


BEAM = [3, 0]
for deformation in DEFORMATIONS:
    MIRROR["deformation"]["amplitude"] = DEFORMATIONS[deformation]

    for num_paxel in [5, 1]:
        SENSOR["num_paxel"] = num_paxel

        beams_to_show = []
        beams_to_show.append(([], [], ""))
        for pix in range(SENSOR["num_pixel"]):
            for pax in range(SENSOR["num_paxel"]):
                beams_to_show.append(([pix], [pax], f"{pix:02d}-{pax:02d}"))

        for beam_to_show in beams_to_show:
            print(beam_to_show)
            fig = splt.Fig(
                cols=FIG_NUM_COLS, rows=int(FIG_NUM_COLS / FIG_RATIO)
            )
            ax = splt.Ax(fig)
            ax["span"] = AXSPAN
            ax["xlim"] = AX_XLIM
            ax["ylim"] = AX_YLIM

            ax_add_scope(
                mirror=MIRROR,
                sensor=SENSOR,
                pixels=beam_to_show[0],
                paxels=beam_to_show[1],
            )

            splt.optics.ax_add_optical_axis(
                ax=ax,
                mirror_diameter=MIRROR["diameter"],
                mirror_focal_length=MIRROR["focal_length"],
                sensor_diameter=SENSOR["diameter"],
                stroke_opacity=0.5,
                stroke_width=2,
                stroke=STROKE,
                overhead=1.1,
            )

            splt.fig_write(
                fig=fig,
                path="scope_P{:d}_{:s}_{:s}{:s}.svg".format(
                    num_paxel, deformation, beam_to_show[2], EXT
                ),
            )
