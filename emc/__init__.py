"""
EarthMC is a large Minecraft server this package lets you get info about things on that server.
"""
from __future__ import annotations

__version__ = "v1.5.1"
__all__ = [
    "__version__",
    "util",
    "exceptions",
    "Resident",
    "Town",
    "Nation",
]

from typing import Dict, Set, Tuple

from shapely.geometry import Polygon

from . import util, exceptions


class Nation:
    """
    A nation

    :param str name: The name of the nation to get
    :param tuple[dict,dict] data: Data from :meth:`emc.util.get_data`
    :raises NationNotFoundException: The nation could not be found
    """
    name: str  #: The name of the nation
    towns: Set[Town]  #: The towns in the nation
    capital: Town  #: The capital of the nation
    leader: Resident  #: The leader of the nation
    colour: str  #: The colour that the towns in the nation appear on the map. Standard hex colour code
    citizens: Set[Resident]  #: The citizens of the nation
    area: int  #: The area of the nation

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
        self.towns = {Town._with_nation(town, data, self) for town in towns}
        self.capital = next(
            (town for town in self.towns if town.flags["capital"]))
        self.leader = self.capital.mayor
        self.colour = self.capital.colour
        self.citizens = {citizen for town in self.towns for citizen in
                         town.residents}
        self.area = sum(town.area for town in self.towns)

    @classmethod
    def all(cls, *, data: Tuple[dict, dict] = None) -> Set[Nation]:
        """
        Returns a set of all nations

        :param tuple[dict,dict] data: Data from :meth:`emc.util.get_data`
        :return: A set of all nations
        :rtype: set[emc.Nation]
        """
        if data is None:
            data = util.get_data()
        return {cls(nation, data=data) for nation in {data[0][town]["desc"][0][:-1].split(" (")[-1] for town in data[0]} if nation != ""}

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return (
                "=== {} ===\nTowns: {}\nCapital: {}\nLeader: {}\nColour: {}"
                "\nCitizens: {}\nArea: {}"
        ).format(self.name, ", ".join([town.name for town in self.towns]),
                 self.capital.name, self.leader.name, self.colour,
                 ", ".join([citizen.name for citizen in self.citizens]),
                 self.area)


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
    residents: List[Resident]  #: The residents of the town
    flags: Dict[str, bool]  #: The flags of the town. pvp, mobs, explosions, fire, capital
    area: int  #: The area of the town
    position: Tuple[int, int]  #: The position of the center of the town
    bounds: util.Bounds  #: The bounds of the town
    ruins: bool  #: True if this town in ruins, otherwise False

    def __init__(self, name: str, *,
                 data: Tuple[dict, dict] = None):
        if data is None:
            data = util.get_data()
        name = name.lower()
        if name not in data[0]:
            raise exceptions.TownNotFoundException(
                "The town {} could not be found".format(name))
        self.name = data[0][name]["label"]
        if not hasattr(self, "nation"):
            nation = data[0][name]["desc"][0][:-1].split("(")[-1]
            if nation == "":
                self.nation = None
            else:
                self.nation = Nation(nation, data=data)
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
        polygon = Polygon(zip(data[0][name]["x"], data[0][name]["z"]))
        self.area = int(polygon.area // 256)
        self.bounds = util.Bounds(*map(int, polygon.bounds))
        self.position = ((self.bounds.max_x+self.bounds.min_x) // 2, (self.bounds.max_y+self.bounds.min_y) // 2)
        self.ruins = len(self.residents) == 1 and self.mayor.npc and self.flags == {"pvp": True, "mobs": True, "explosions": True, "fire": True,
                                                                                    "capital": False}

    @classmethod
    def _with_nation(cls, name, data, nation):
        town = cls.__new__(cls)
        town.nation = nation
        town.__init__(name, data=data)
        return town

    @classmethod
    def all(cls, *, data: Tuple[dict, dict] = None) -> Set[Town]:
        """
        Returns a set of all towns

        :param tuple[dict,dict] data: Data from :meth:`emc.util.get_data`
        :return: A set of all towns
        :rtype: set[emc.Town]
        """
        if data is None:
            data = util.get_data()
        return {cls(town, data=data) for town in data[0]}

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return (
                "=== {0} ===\ncolour: {1}\nmayor: {2}\nresidents: {3}\nnation: {4}\n"
                "Area: {6}\nPosition: {7}\nBounds: ({8.min_x}-{8.max_x}, {8.min_y}-{8.max_y})\n"
                "--- flags ---\npvp: {5[pvp]}\nmobs: {5[mobs]}\n"
                "explosions: {5[explosions]}\nfire: {5[fire]}\ncapital: {5[capital]}"
        ).format(self.name, self.colour, self.mayor.name,
                 ", ".join([person.name for person in self.residents]),
                 self.nation.name, self.flags, self.area, self.position, self.bounds)


class Resident:
    """
    A person

    :param str name: The name of the resident to search for
    :param tuple[dict,dict] data: Data from :meth:`emc.util.get_data`
    """
    name: str  #: The name of the resident
    online: bool  #: Weather or not the resident is online
    position: Tuple[int, int, int]  #: The position of the resident, (0, 64, 0) if hidden == True or None if online == False
    hidden: bool  #: Weather or not the resident can be seen on the map
    town: Town  #: The town that the resident belongs to, None if the resident is townless
    nation: Nation  #: The nation that the resident's town is in, None if the resident is townless or the town nationless
    npc: bool  #: Is this resident an NPC?

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
        if not hasattr(self, "town"):
            self.town = next((Town(town_name, data=data) for town_name in data[0] if
                              name in data[0][town_name]["desc"][4]), None)
        if self.town is None:
            self.nation = None
        else:
            self.nation = self.town.nation
        self.npc = self.name.startswith("NPC") and self.name[3:].isdigit()

    @classmethod
    def _with_town(cls, name, data, town):
        resident = cls.__new__(cls)
        resident.town = town
        resident.__init__(name, data=data)
        return resident

    @classmethod
    def all_online(cls, *, data: Tuple[dict, dict] = None) -> Set[Resident]:
        """
        Returns a set of all online players

        :param tuple[dict,dict] data: Data from :meth:`emc.util.get_data`
        :return: Set of all online players
        :rtype: set[emc.Resident]
        """
        if data is None:
            data = util.get_data()
        return {cls(resident["account"], data=data) for resident in data[1]["players"]}

    @classmethod
    def all(cls, *, data: Tuple[dict, dict] = None) -> Set[Resident]:
        """
        Returns a set of all players who are in a town

        :param tuple[dict,dict] data: Data from :meth:`emc.util.get_data`
        :return: Set of all players who are in a town
        :rtype: set[emc.Resident]
        """
        if data is None:
            data = util.get_data()
        return {resident for town in Town.all(data=data) for resident in town.residents}

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return (
                "=== {} ===\nOnline: {}\nPosition: {}\n"
                "Hidden: {}\nTown: {}\nNation: {}"
        ).format(self.name, self.online, self.position,
                 self.hidden, self.town, self.nation)
