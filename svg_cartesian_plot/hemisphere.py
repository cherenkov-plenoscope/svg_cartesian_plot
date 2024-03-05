from . import base
from . import shapes
from . import color
import numpy as np


def Ax(fig):
    ax = base.Ax(fig=fig)
    ax["xlim"] = [-1, 1]
    ax["ylim"] = [-1, 1]
    return ax


def ax_add_grid(ax, **kwargs):
    ax_add_grid_lines_stellarium_style(ax=ax, **kwargs)

    if "stroke" in kwargs:
        fill = kwargs["stroke"]
    else:
        fill = None

    ax_add_ticklabel_text(
        ax=ax,
        font_family="math",
        fill=fill,
        **kwargs,
    )


def ax_add_grid_lines_stellarium_style(ax, **kwargs):
    TAU = 2.0 * np.pi
    ax_add_grid_lines(
        ax=ax,
        azimuths_rad=np.linspace(0, TAU, 36, endpoint=False),
        zeniths_rad=np.deg2rad([0, 10, 20, 30, 40, 50, 60, 70, 80, 90]),
        zenith_min_rad=np.deg2rad(5),
        **kwargs,
    )


def ax_add_grid_lines(
    ax, azimuths_rad, zeniths_rad, zenith_min_rad=0.0, **kwargs
):
    zeniths = zeniths_rad
    zenith_min = zenith_min_rad

    proj_radii = np.sin(zeniths)
    for i in range(len(zeniths)):
        shapes.ax_add_circle(
            ax=ax,
            xy=[0, 0],
            radius=proj_radii[i],
            **kwargs,
        )

    azimuths = azimuths_rad
    for a in range(len(azimuths)):
        for z in range(len(zeniths)):
            if z == 0:
                continue
            zzstart = np.max([zenith_min, zeniths[z - 1]])
            r_start = np.sin(zzstart)
            zzstop = np.max([zenith_min, zeniths[z]])
            r_stop = np.sin(zzstop)
            start_x = r_start * np.cos(azimuths[a])
            start_y = r_start * np.sin(azimuths[a])
            stop_x = r_stop * np.cos(azimuths[a])
            stop_y = r_stop * np.sin(azimuths[a])
            base.ax_add_line(
                ax=ax,
                xy_start=[start_x, start_y],
                xy_stop=[stop_x, stop_y],
                **kwargs,
            )


def ax_add_ticklabel_text(
    ax,
    radius=0.9,
    label_azimuths_rad=[0, 1 / 2 * np.pi, 2 / 2 * np.pi, 3 / 2 * np.pi],
    label_azimuths=["N", "E", "S", "W"],
    xshift=-0.0,
    yshift=-0.0,
    **kwargs,
):
    for i in range(len(label_azimuths_rad)):
        _az = label_azimuths_rad[i]
        xs = radius * (np.cos(_az) + xshift)
        ys = radius * (np.sin(_az) + yshift)
        base.ax_add_text(
            ax=ax,
            xy=1.05 * np.array([xs, ys]),
            r=90 + np.rad2deg(label_azimuths_rad[i]),
            **kwargs,
            text=label_azimuths[i],
        )


def ax_add_grid_text(
    ax, zenith_step_deg=15, azimuth_step_deg=30, radius=1.0, **kwargs
):
    for az_deg in np.arange(0, 360, azimuth_step_deg):
        az = np.deg2rad(az_deg)
        start = radius * np.array([np.cos(az), np.sin(az)])
        base.ax_add_text(
            ax=ax,
            xy=1.05 * start,
            r=0.0,
            **kwargs,
            text="{: 3.0f}".format(az_deg),
        )


def init_mesh_look(
    num_faces,
    stroke=color.css("black"),
    stroke_width=1.0,
    stroke_opacity=1,
    fill=color.css("aqua"),
    fill_opacity=1,
):
    out = {}
    out["faces_stroke"] = [stroke for i in range(num_faces)]
    out["faces_stroke_width"] = [stroke_width for i in range(num_faces)]
    out["faces_stroke_opacity"] = [stroke_opacity for i in range(num_faces)]
    out["faces_fill"] = [fill for i in range(num_faces)]
    out["faces_fill_opacity"] = [fill_opacity for i in range(num_faces)]
    return out


def ax_add_mesh(
    ax,
    vertices,
    faces,
    faces_stroke=None,
    faces_stroke_width=None,
    faces_stroke_opacity=None,
    faces_fill=None,
    faces_fill_opacity=None,
    max_radius=1.0,
    **kwargs,
):
    if faces_stroke:
        assert len(faces_stroke) == len(faces)
    else:
        faces_stroke = [color.css("black") for i in range(len(faces))]

    if faces_stroke_width:
        assert len(faces_stroke_width) == len(faces)
    else:
        faces_stroke_width = [1.0 for i in range(len(faces))]

    if faces_fill:
        assert len(faces_fill) == len(faces)
    else:
        faces_fill = [color.css("aqua") for i in range(len(faces))]

    if faces_fill_opacity:
        assert len(faces_fill_opacity) == len(faces)
    else:
        faces_fill_opacity = [1 for i in range(len(faces))]

    if faces_stroke_opacity:
        assert len(faces_stroke_opacity) == len(faces)
    else:
        faces_stroke_opacity = [1 for i in range(len(faces))]

    for fidx in range(len(faces)):
        face_vertices = []
        face = faces[fidx]
        for vidx in face:
            if vidx != -1:
                vertex_i = vertices[vidx]
                vertex_i_norm = np.linalg.norm(vertex_i)
                if vertex_i_norm > max_radius:
                    vertex_i = vertex_i * max_radius / vertex_i_norm

                face_vertices.append(vertex_i)

        if len(face_vertices) >= 3:
            face_first_vertex = face_vertices[0]
            face_vertices.append(face_first_vertex)
            base.ax_add_path(
                ax=ax,
                xy=face_vertices,
                stroke=faces_stroke[fidx],
                stroke_width=faces_stroke_width[fidx],
                stroke_opacity=faces_stroke_opacity[fidx],
                fill=faces_fill[fidx],
                fill_opacity=faces_fill_opacity[fidx],
                **kwargs,
            )
