from setuptools import setup
from os import listdir

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="EMC-info",
    version="1.0",
    description="EarthMC is a large Minecraft server this package lets you get info about things on that server.",
    py_modules=[module[-2] for module in listdir("emc") if module.endswith(".py")],
    package_dir={"": "emc"},
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
    ],
    url="https://github.com/TheSuperGamer20578/EMC-info/wiki",
    author="TheSuperGamer20578",
    install_requires=[],
)
