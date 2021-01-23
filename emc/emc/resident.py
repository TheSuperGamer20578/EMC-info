"""
stuff about residents
"""
import requests
from typing import Tuple

from . import util, town, nation


class PlayerNotFoundError(Exception):
    """
    exception for when a player cant be found
    """


class Resident:
    """
    a person
    """

    def __init__(self, name: str, *, data: Tuple[dict, dict] = util.get_data(),
                 _town: town.Town = None):
        minecraft = requests.get(
            "https://api.mojang.com/users/profiles/minecraft/" + name)
        if minecraft.status_code != 200:
            raise PlayerNotFoundError(
                "The user {} was not found on Mojang's api or there was some other error: {}".format(
                    name, minecraft.status_code))
        res_data = next((person for person in data[1]["players"] if
                         person["name"] == name), None)
        self.name = name
        self.uuid = minecraft.json()["id"]
        if res_data is not None:
            self.online = True
            self.position = (res_data["x"], res_data["y"], res_data["z"])
            self.hidden = True if self.position == (0, 64, 0) else False
        self.town = town.Town([town_name for town_name in data[0] if
                               name in data[0][town_name]["desc"][4]][0],
                              data=data) or None
        self.nation = self.town.nation or None
        self.online = False
        self.position = None
        self.hidden = True

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return (
                "=== {} ===\nUUID: {}\nOnline: {}\nPosition: {3[0]}/{3[1]}/{3[2]}\n" +
                "Hidden: {}\nTown: {}\nNation: {}"
        ).format(self.name, self.uuid, self.online, self.position,
                 self.hidden, self.town, self.nation)
