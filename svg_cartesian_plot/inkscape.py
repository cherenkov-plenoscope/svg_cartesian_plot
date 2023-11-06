import subprocess


def render(svg_path, out_path, background_opacity=0.0, export_type="png"):
    rc = subprocess.call(
        [
            "inkscape",
            "--export-background-opacity={:f}".format(background_opacity),
            "--export-type={:s}".format(export_type),
            "--export-filename={:s}".format(out_path),
            svg_path,
        ]
    )
