import svg_cartesian_plot as splt


def test_example():
    fig = splt.Fig(cols=1920, rows=1080)
    ax = splt.Ax(fig)

    splt.ax_add_line(
        ax=ax,
        xy_start=(0, 0),
        xy_stop=(1, 1),
        stroke=(200, 30, 30),
        stroke_width=5,
        stroke_linecap="round",
        stroke_opacity=1.0,
    )
    splt.ax_add_path(
        ax=ax,
        xy=[[0.0, 0.0], [0.5, 1.0], [1, 1]],
        stroke=(200, 20, 20),
        stroke_width=8,
        stroke_opacity=0.5,
        fill=(1, 2, 30),
        fill_opacity=0.5,
    )

    splt.ax_add_text(
        ax=ax,
        xy=[0.5, 0.5],
        text="10=1.337",
        fill=[0, 0, 200],
        font_family="math",
        font_size=60,
    )

    splt.fig_write(fig=fig, path="test.svg")
    splt.fig_write(fig=fig, path="test.jpg")
