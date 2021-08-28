import re
from setuptools import setup, find_packages

with open("README.md") as fh:
    long_description = fh.read()

with open("emc/__init__.py") as file:
    pattern = re.compile(r'^__version__ = "v(\d*[1-9]\.\d*[1-9](?:\.\d*[1-9])*)(?:-((?:rc|b|a)\d+))?"$')
    for line in file:
        match = pattern.match(line)
        if match is None:
            continue
        version = match.group(1) + (match.group(2) if match.group(2) is not None else "")
        break
    else:
        raise RuntimeError("Could not find version in emc/__init__.py")

setup(
    name="EMC-info",
    version=version,
    description="EarthMC is a large Minecraft server this package lets you get info about things on that server.",
    packages=["emc"],
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
    install_requires=[
        "requests",
        "shapely",
    ],
    tests_require=["pytest", "pytest-asyncio"],
    test_suite="pytest test.py",
    extras_require={
        "async": ["aiohttp"]
    }
)
