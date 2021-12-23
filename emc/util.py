"""
Utilities to help with other modules
"""
from typing import Tuple, Any
from re import split
from collections import namedtuple

from requests import get

_headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"}

Bounds = namedtuple("Bounds", ("min_x", "min_y", "max_x", "max_y"))  #: Namedtuple that represents the bounds of a town


def map_link(position: Tuple[float, Any, float], zoom: int = 6) -> str:
    """
    Return a link to the map at the specified position

    :param tuple[float,Any,float] position: The position to return a map link to, only the first and last items are used
    :param int zoom: The zoom level, must be between 0 and 8
    :return: The link to the map
    :rtype: str
    """
    return ("https://earthmc.net/map/?zoom={}&x={}&z={}"
            .format(zoom, position[0], position[-1]))


def get_data() -> Tuple[dict, dict]:
    """
    Returns the map data. Useful for making multiple requests

    :raises requests.HTTPError: Could not get data
    :return: The map data
    :rtype: tuple[dict,dict]
    """
    resp_town = get("https://earthmc.net/map/tiles/_markers_/marker_earth.json",
                    headers=_headers)
    resp_town.raise_for_status()
    resp_player = get("https://earthmc.net/map/up/world/earth/",
                      headers=_headers)
    resp_player.raise_for_status()
    town_data = resp_town.json()["sets"]["townyPlugin.markerset"]["areas"]
    towns = {
      name[:-3].lower(): town[1] for name, town in zip(town_data, town_data.items()) if name.endswith("__0")
      }
    for town in towns:
        towns[town]["desc"] = [desc for desc in split(r"<[^<>]*>", towns[town]["desc"]) if desc != ""]
    return towns, resp_player.json()
