"""
nation stuff
"""
from typing import Tuple

from . import util, town, resident


class NationNotFoundError(Exception):
    """
    raised when a nation could not be found
    """


class Nation:
    """
    A nation
    """
    def __init__(self, name: str, *, data: Tuple[dict, dict] = util.get_data()):
        towns = [t for t in data[0] if data[0][t]["desc"][0][:-1].split(" (")[-1] == name]
        if len(towns) <= 0:
            raise NationNotFoundError("The nation {} was not found".format(name))
        self.name = name
        self.towns = [town.Town(t) for t in towns]
        self.capital = next((t for t in self.towns if t.flags["capital"]))
        self.leader = self.capital.mayor
        self.colour = self.capital.colour
        self.citizens = [citizen for t in self.towns for citizen in t.residents]

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return (
                "=== {} ===\nTowns: {}\nCapital: {}\nLeader: {}\nColour: {}" +
                "Citizens: {}"
        ).format(self.name, ", ".join([t.name for t in self.towns]),
                 self.capital.name, self.leader.name, self.colour,
                 ", ".join([citizen.name for citizen in self.citizens]))
