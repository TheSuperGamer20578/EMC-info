"""
EarthMC is a large Minecraft server this package lets you get info about things on that server.
"""
from __future__ import annotations

from typing import Tuple

from . import util, exceptions

__version__ = "v1.2"
__all__ = [
    "__version__",
    "util",
    "exceptions",
    "Resident",
    "Town",
    "Nation",
]


class Nation:
    """
    A nation

    :param str name: The name of the nation to get
    :param tuple[dict,dict] data: Data from :meth:`emc.util.get_data`
    :raises NationNotFoundException: The nation could not be found
    """
    name: str  #: The name of the nation
    towns: list[Town]  #: The towns in the nation
    capital: Town  #: The capital of the nation
    leader: Resident  #: The leader of the nation
    colour: str  #: The colour that the towns in the nation appear on the map. Standard hex colour code
    citizens: list[Resident]  #: The citizens of the nation

    def __init__(self, name: str, *,
                 data: Tuple[dict, dict] = None):
        if data is None:
            data = util.get_data()
        towns = [town for town in data[0] if
                 data[0][town]["desc"][0][:-1].split(" (")[-1] == name]
        if len(towns) <= 0 or name == "":
            raise exceptions.NationNotFoundException(
                "The nation {} was not found".format(name))
        self.name = name
        self.towns = [Town._with_nation(town, data, self) for town in towns]
        self.capital = next(
            (town for town in self.towns if town.flags["capital"]))
        self.leader = self.capital.mayor
        self.colour = self.capital.colour
        self.citizens = [citizen for town in self.towns for citizen in
                         town.residents]

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return (
                "=== {} ===\nTowns: {}\nCapital: {}\nLeader: {}\nColour: {}" +
                "\nCitizens: {}"
        ).format(self.name, ", ".join([town.name for town in self.towns]),
                 self.capital.name, self.leader.name, self.colour,
                 ", ".join([citizen.name for citizen in self.citizens]))


class Town:
    """
    A town

    :param str name: The name of the town to look for
    :param tuple[dict,dict] data: Data from :meth:`emc.util.get_data`
    :raises TownNotFoundException: The town could not be found
    """
    name: str  #: The name of the town
    nation: Nation  #: The nation the town is in or None if the town is nationless
    colour: str  #: The colour that the town appears on the map. Standard hex colour code
    mayor: Resident  #: The mayor of the town
    residents: list[Resident]  #: The residents of the town
    flags: dict[str, bool]  #: The flags of the town. pvp, mobs, explosions, fire, capital

    def __init__(self, name: str, *,
                 data: Tuple[dict, dict] = None):
        if data is None:
            data = util.get_data()
        name = name.lower()
        if name not in data[0]:
            raise exceptions.TownNotFoundException(
                "The town {} could not be found".format(name))
        self.name = data[0][name]["label"]
        if self.nation is None:
            self.nation = Nation(
                data[0][name]["desc"][0][:-1].split("(")[-1],
                data=data) or None
        self.colour = data[0][name]["fillcolor"]
        self.mayor = Resident._with_town(data[0][name]["desc"][2], data, self)
        self.residents = [Resident._with_town(person, data, self)
                          for person in data[0][name]["desc"][4].split(", ")]
        self.flags = {
            "pvp": data[0][name]["desc"][7] == "pvp: true",
            "mobs": data[0][name]["desc"][8] == "mobs: true",
            "explosions": data[0][name]["desc"][10] == "explosion: true",
            "fire": data[0][name]["desc"][11] == "fire: true",
            "capital": data[0][name]["desc"][12] == "capital: true"
        }

    @classmethod
    def _with_nation(cls, name, data, nation):
        town = cls.__new__(cls)
        town.nation = nation
        town.__init__(name, data=data)
        return town

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return (
                "=== {0} ===\ncolour: {1}\nmayor: {2}\nresidents: {3}\nnation: {4}\n" +
                "--- flags ---\npvp: {5[pvp]}\nmobs: {5[mobs]}\n" +
                "explosions: {5[explosions]}\nfire: {5[fire]}\ncapital: {5[capital]}"
        ).format(self.name, self.colour, self.mayor.name,
                 ", ".join([person.name for person in self.residents]),
                 self.nation.name, self.flags)


class Resident:
    """
    A person

    :param str name: The name of the resident to search for
    :param tuple[dict,dict] data: Data from :meth:`emc.util.get_data`
    :param town: Internal use only, will be removed in v1.3
    """
    name: str  #: The name of the resident
    online: bool  #: Weather or not the resident is online
    position: tuple[int, int, int]  #: The position of the resident, (0, 64, 0) if hidden == True
    hidden: bool  #: Weather or not the resident can be seen on the map
    town: Town  #: The town that the resident belongs to, None if the resident is townless
    nation: Nation  #: The nation that the resident's town is in, None if the resident is townless or the town nationless

    def __init__(self, name: str, *, data: Tuple[dict, dict] = None):
        if data is None:
            data = util.get_data()
        res_data = next((person for person in data[1]["players"] if
                         person["account"] == name), None)
        self.name = name
        if res_data is not None:
            self.online = True
            self.position = (res_data["x"], res_data["y"], res_data["z"])
            self.hidden = self.position == (0, 64, 0)
        else:
            self.online = False
            self.position = None
            self.hidden = True
        if self.town is None:
            self.town = Town([town_name for town_name in data[0] if
                              name in data[0][town_name]["desc"][4]][0],
                             data=data) or None
        self.nation = self.town.nation or None

    @classmethod
    def _with_town(cls, name, data, town):
        resident = cls.__new__(cls)
        resident.town = town
        resident.__init__(name, data=data)
        return resident

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return (
                "=== {} ===\nOnline: {}\nPosition: {}\n" +
                "Hidden: {}\nTown: {}\nNation: {}"
        ).format(self.name, self.online, self.position,
                 self.hidden, self.town, self.nation)
