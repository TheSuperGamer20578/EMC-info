"""
EarthMC is a large Minecraft server this package lets you get info about things on that server.
"""
from typing import Tuple

from . import util, exceptions

__all__ = [
    "util",
    "exceptions",
    "Resident",
    "Town",
    "Nation"
]


class Nation:
    """
    A nation
    """

    def __init__(self, name: str, *,
                 data: Tuple[dict, dict] = None):
        if data is None:
            data = util.get_data()
        towns = [town for town in data[0] if
                 data[0][town]["desc"][0][:-1].split(" (")[-1] == name]
        if len(towns) <= 0:
            raise exceptions.NationNotFoundException(
                "The nation {} was not found".format(name))
        self.name = name
        self.towns = [Town(town, data=data, nation=self) for town in towns]
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
    """

    def __init__(self, name: str, *,
                 data: Tuple[dict, dict] = None,
                 nation: Nation = None):
        if data is None:
            data = util.get_data()
        if name not in data[0]:
            raise exceptions.TownNotFoundException(
                "The town {} could not be found".format(name))
        self.name = data[0][name]["label"]
        if nation is not None:
            self.nation = nation
        else:
            self.nation = Nation(
                data[0][name]["desc"][0][:-1].split("(")[-1],
                data=data) or None
        self.colour = data[0][name]["fillcolor"]
        self.mayor = Resident(data[0][name]["desc"][2], data=data,
                              town=self)
        self.residents = [Resident(person, data=data, town=self)
                          for person in data[0][name]["desc"][4].split(", ")]
        self.flags = {
            "pvp": data[0][name]["desc"][7],
            "mobs": data[0][name]["desc"][8],
            "explosions": data[0][name]["desc"][10],
            "fire": data[0][name]["desc"][11],
            "capital": data[0][name]["desc"][12]
        }

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return (
                "=== {0} ===\ncolour: {1}\nmayor: {2}\nresidents: {3}\nnation: {4}\n" +
                "--- flags ---\n{5[pvp]}\n{5[mobs]}\n{5[explosions]}\n{5[fire]}\n" +
                "{5[capital]}"
        ).format(self.name, self.colour, self.mayor.name,
                 ", ".join([person.name for person in self.residents]),
                 self.nation.name, self.flags)


class Resident:
    """
    a person
    """

    def __init__(self, name: str, *, data: Tuple[dict, dict] = None,
                 town: Town = None):
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
        if town is not None:
            self.town = town
        else:
            self.town = Town([town_name for town_name in data[0] if
                              name in data[0][town_name]["desc"][4]][0],
                             data=data) or None
        self.nation = self.town.nation or None

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return (
                "=== {} ===\nOnline: {}\nPosition: {}\n" +
                "Hidden: {}\nTown: {}\nNation: {}"
        ).format(self.name, self.online, self.position,
                 self.hidden, self.town, self.nation)
