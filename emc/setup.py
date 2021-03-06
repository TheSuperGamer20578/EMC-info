from setuptools import setup, find_packages
from os import listdir

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="EMC-info",
    version="1.1-rc1",
    description="EarthMC is a large Minecraft server this package lets you get info about things on that server.",
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Topic :: Games/Entertainment",
        "Typing :: Typed"
    ],
    url="https://github.com/TheSuperGamer20578/EMC-info/",
    author="TheSuperGamer20578",
    install_requires=["requests"],
    extras_require = {
        "async": ["aiohttp"]
    }
)
