import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="svgplot_sebastian-achim-mueller",
    version="0.0.1",
    author="Sebastian Achim Mueller",
    author_email="sebastian-achim.mueller@mpi-hd.mpg.de",
    description="Make plots in scalable vector graphics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/relleums",
    install_requires=["svgwrite"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Multimedia :: Graphics",
        "Intended Audience :: Science/Research",
    ],
    packages=["svgplot",],
    python_requires=">=3.0",
)
