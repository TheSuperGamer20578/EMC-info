![Version](https://badge.fury.io/py/EMC-info.svg)  
EarthMC is a large Minecraft server this package lets you get info about things on that server.  
[PyPI](https://pypi.org/project/EMC-info) **|** [Github](https://github.com/TheSuperGamer20578/EMC-info) **|** [Changelog](https://github.com/TheSuperGamer20578/EMC-info/releases) | [Documentation](https://emc-info.readthedocs.io/en/stable/)

## Installation
```shell
pip install EMC-info
```

## Usage
Importing:
```py
import emc
```
Getting info about a town and printing its mayor's name:
```py
town = emc.Town("town")
print(town.mayor.name)
```
Read the [documentation](https://emc-info.readthedocs.io/en/stable/) for more information
