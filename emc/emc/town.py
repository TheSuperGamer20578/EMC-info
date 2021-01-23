"""
contains town class and town not found error
"""
from typing import Tuple

from . import util, resident, nation


class TownNotFoundError(Exception):
    """
    Exception for when a town cant be found
    """


class Town:
    """
    A town
    """

    def __init__(self, name: str, *,
                 data: Tuple[dict, dict] = util.get_data(),
                 _nation: nation.nation = None):
        if name not in data[0]:
            raise TownNotFoundError(
                "The town {} could not be found".format(name))
        self.name = data[0][name]["label"]
        if _nation is not None:
            self.nation = _nation
        else:
            self.nation = nation.Nation(
                data[0][name]["desc"][0][:-1].split("(")[-1], data=data) or None
        self.colour = data[0][name]["fillcolor"]
        self.mayor = resident.Resident(data[0][name]["desc"][2], data=data,
                                       _town=self)
        self.residents = [resident.Resident(person, data=data, _town=self)
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
                "=== {} ===\ncolour: {}\nmayor: {}\nresidents: {}\nnation: {}\n" +
                "\n--- flags ---\npvp: {5['pvp']}\nmobs: {5['mobs']}\n" +
                "explosions: {5['explosions']}\nfire: {5['fire']}\n" +
                "capital: {5['capital']}"
        ).format(self.name, self.colour, self.mayor.name,
                 ", ".join([person.name for person in self.residents]),
                 self.nation.name, self.flags)
