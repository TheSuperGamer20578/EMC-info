from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="EMC-info",
    version="0.1",
    description="EarthMC is a large Minecraft server this package lets you get info about things on that server.",
    py_modules=["EMC"],
    package_dir={"": "src"},
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
    ],
    url="https://github.com/TheSuperGamer20578/EMC-info/wiki",
    author="TheSuperGamer20578",
    author_email="emc@thesupergamer20578.ml"
)
