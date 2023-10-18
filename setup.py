import setuptools
import os

with open("README.rst", "r", encoding="utf-8") as f:
    long_description = f.read()


with open(os.path.join("svgplot", "version.py")) as f:
    txt = f.read()
    last_line = txt.splitlines()[-1]
    version_string = last_line.split()[-1]
    version = version_string.strip("\"'")


setuptools.setup(
    name="svgplot_sebastian-achim-mueller",
    version=version,
    author="Sebastian Achim Mueller",
    author_email="sebastian-achim.mueller@mpi-hd.mpg.de",
    description="Make plots in scalable vector graphics",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/cherenkov-plenoscope/svgplot",
    packages=[
        "svgplot",
    ],
    package_data={"svgplot": []},
    install_requires=["svgwrite"],
    classifiers=[
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Multimedia :: Graphics",
        "Intended Audience :: Science/Research",
    ],
    python_requires=">=3.0",
)
