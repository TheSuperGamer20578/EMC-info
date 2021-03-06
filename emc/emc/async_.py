"""Async implementation of get_data"""
from typing import Tuple
from re import split

from aiohttp import ClientSession

HEADERS = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"}

URL_TOWN = "https://earthmc.net/map/tiles/_markers_/marker_earth.json"
URL_PLAYER = "https://earthmc.net/map/up/world/earth/"


async def get_data() -> Tuple[dict, dict]:
    """Returns the map data"""
    async with ClientSession() as session:
        async with session.get(URL_TOWN, headers=HEADERS) as resp_town, \
                session.get(URL_PLAYER, headers=HEADERS) as resp_player:
            if not resp_town.status == 200 == resp_player.status:
                return await get_data
            town_data = (await resp_town.json(content_type="text/plain"))["sets"]["townyPlugin.markerset"]["areas"]
            towns = {
                name[:-3]: town[1] for name, town in zip(town_data, town_data.items()) if name.endswith("__0")
            }
            for town in towns:
                towns[town]["desc"] = [desc for desc in split(r"<[^<>]*>", towns[town]["desc"]) if desc != ""]
            return towns, await resp_player.json(content_type="text/plain")

