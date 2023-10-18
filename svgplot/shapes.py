from . import base as splt
import numpy as np


def ax_add_circle(
    ax,
    xy,
    radius,
    fn=101,
    **kwargs,
):
    phis = np.linspace(0, 2*np.pi, fn)
    for i in range(fn - 1):
        start = radius * np.array([np.cos(phis[i]), np.sin(phis[i])])
        stop = radius * np.array([np.cos(phis[i+1]), np.sin(phis[i+1])])
        splt.ax_add_line(ax=ax, xy_start=start, xy_stop=stop, **kwargs)


def ax_add_hemisphere_grid(ax, zenith_step_deg=15, azimuth_step_deg=45, radius=1.0, **kwargs):
    for zd_deg in np.arange(zenith_step_deg, 90+zenith_step_deg, zenith_step_deg):
        ax_add_circle(
            ax=ax,
            xy=[0, 0],
            radius=radius * np.sin(np.deg2rad(zd_deg)),
             **kwargs
        )

    for az_deg in  np.arange(0, 360, azimuth_step_deg):
        az = np.deg2rad(az_deg)
        start = radius * np.array([np.cos(az), np.sin(az)])
        stop = [0, 0]
        splt.ax_add_line(
            ax=ax, xy_start=start, xy_stop=stop, **kwargs
        )


def ax_add_hemisphere_grid_text(ax, zenith_step_deg=15, azimuth_step_deg=45, radius=1.0, **kwargs):
    for az_deg in  np.arange(0, 360, azimuth_step_deg):
        az = np.deg2rad(az_deg)
        start = radius * np.array([np.cos(az), np.sin(az)])
        splt.ax_add_text(
            ax=ax,
            xy=1.05 * start,
            r=0.0, **kwargs,
            text="{: 3.0f}".format(az_deg)
        )
