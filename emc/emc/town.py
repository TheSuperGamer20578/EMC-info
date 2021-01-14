"""
contains town class and town not found error
"""
from typing import Tuple

from . import util


class TownNotFoundError(Exception):
    """
    Exception for when a town cant be found
    """


class Town:
    """
    A town
    """

    def __init__(self, name: str, *,
                 data: Tuple[dict, dict] = util.get_data()):
        if name not in data[0]:
            raise TownNotFoundError(
                "The town {} could not be found".format(name))
        self.name = data[0][name]["label"]
        self.colour = data[0][name]["fillcolor"]
        self.mayor = residents.Resident(data[0][name]["desc"][2], data=data,
                                        town=self)
        self.residents = [residents.Resident(resident, data=data, town=self)
                          for resident in data[0][name]["desc"][4].split(", ")]
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
        return ("=== {} ===\ncolour: {}\nmayor: {}\nresidents: {}\n" +
                "\n--- flags ---\npvp: {4['pvp']}\nmobs: {4['mobs']}\n" +
                "explosions: {4['explosions']}\nfire: {4['fire']}\n" +
                "capital: {4['capital']}")
