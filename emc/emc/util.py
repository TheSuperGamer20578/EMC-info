"""
Utilitys to help with other moduls
"""
from typing import Tuple, Any
from re import split
from requests import get

_headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"}


def map_link(position: Tuple[float, Any, float], zoom: int = 6) -> str:
    """
    Returns a link to the map at the specified position
    """
    return ("https://earthmc.net/map/?zoom={}&x={}&z={}"
            .format(zoom, position[0], position[-1]))


def get_data() -> Tuple[dict, dict]:
    """
    Returns the map data
    """
    resp_town = get("https://earthmc.net/map/tiles/_markers_/marker_earth.json",
                    headers=_headers)
    resp_player = get("https://earthmc.net/map/up/world/earth/",
                      headers=_headers)
    if not resp_town.status_code == 200 == resp_player.status_code:
        return get_data()
    town_data = resp_town.json()["sets"]["townyPlugin.markerset"]["areas"]
    towns = {
      name[:-3]: town[1] for name, town in zip(town_data, town_data.items()) if name.endswith("__0")
      }
    for town in towns:
        towns[town]["desc"] = [desc for desc in split(r"<[^<>]*>", towns[town]["desc"]) if desc != ""]
    return towns, resp_player.json()
