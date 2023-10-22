from . import base
from . import shapes
from . import color
import numpy as np


def Ax(fig):
    ax = base.Ax(fig=fig)
    ax["xlim"] = [-1, 1]
    ax["ylim"] = [-1, 1]
    return ax


def ax_add_grid(ax):
    ax_add_grid_lines(
        ax=ax,
        zenith_step_deg=15,
        azimuth_step_deg=45,
        radius=1.0,
        stroke=color.css("gray"),
    )
    ax_add_grid_text(
        ax=ax,
        zenith_step_deg=15,
        azimuth_step_deg=45,
        radius=1.0,
        stroke=color.css("black"),
        font_family="math",
        font_size=15,
    )


def ax_add_grid_lines(
    ax, zenith_step_deg=15, azimuth_step_deg=45, radius=1.0, **kwargs
):
    for zd_deg in np.arange(
        zenith_step_deg, 90 + zenith_step_deg, zenith_step_deg
    ):
        shapes.ax_add_circle(
            ax=ax,
            xy=[0, 0],
            radius=radius * np.sin(np.deg2rad(zd_deg)),
            **kwargs,
        )

    for az_deg in np.arange(0, 360, azimuth_step_deg):
        az = np.deg2rad(az_deg)
        start = radius * np.array([np.cos(az), np.sin(az)])
        stop = [0, 0]
        base.ax_add_line(ax=ax, xy_start=start, xy_stop=stop, **kwargs)


def ax_add_grid_text(
    ax, zenith_step_deg=15, azimuth_step_deg=45, radius=1.0, **kwargs
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
    stroke_opacity=1,
    fill=color.css("aqua"),
    fill_opacity=1,
):
    out = {}
    out["faces_stroke"] = [stroke for i in range(num_faces)]
    out["faces_stroke_opacity"] = [stroke_opacity for i in range(num_faces)]
    out["faces_fill"] = [fill for i in range(num_faces)]
    out["faces_fill_opacity"] = [fill_opacity for i in range(num_faces)]
    return out


def ax_add_mesh(
    ax,
    vertices,
    faces,
    faces_stroke=None,
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
                stroke_opacity=faces_stroke_opacity[fidx],
                fill=faces_fill[fidx],
                fill_opacity=faces_fill_opacity[fidx],
                **kwargs,
            )
