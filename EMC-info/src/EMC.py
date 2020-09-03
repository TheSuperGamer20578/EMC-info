import json
import re
import aiohttp
import urllib.request


async def a_get_data():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://earthmc.net/map/up/world/earth/') as resp:
            if resp.status == 200:
                rdata = json.loads(await resp.text())
            else:
                return await a_get_data()
        async with session.get('https://earthmc.net/map/tiles/_markers_/marker_earth.json') as resp:
            if resp.status == 200:
                tdata = json.loads(await resp.text())
            else:
                return await a_get_data()
    data = (rdata, tdata)
    return data


def get_data():
    data = (
        json.loads(urllib.request.urlopen(
            urllib.request.Request(url="https://earthmc.net/map/up/world/earth/", headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'})).read().decode()),
        json.loads(urllib.request.urlopen(
            urllib.request.Request(url="https://earthmc.net/map/tiles/_markers_/marker_earth.json", headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'})).read().decode()))
    return data


# noinspection PyUnusedLocal
def onlineResidents(data: tuple = None):
    for x in rdata["players"]:
        yield Resident(x["name"], data)


class Resident:
    def __init__(self, name: str, data: tuple = None, town=None):
        if data is None:
            data = get_data()
        rdata, tdata = data[0], data[1]
        t = tdata["sets"]["townyPlugin.markerset"]["areas"]
        for x in t:
            if x.endswith("__0"):
                desc = re.sub("<[^>]+>", "||", t[x]["desc"])
                desc = desc.split("||")
                for i, v in enumerate(desc):
                    if v == "":
                        del desc[i]
                if x.endswith("__0") and name in desc[5].split(", "):
                    if town:
                        self.town = town
                    else:
                        self.town = Town(x[:-3], data)
                    # if not self.town.nationless:
                    #     self.nation = self.town.nation
                    self.townless = False
                    break
        else:
            self.townless = True
        for x in rdata["players"]:
            if x["name"] == name:
                r = x
                self.pos = r["x"], r["y"], r["z"]
                self.online = True
                break
        else:
            self.online = False
        self.name = name


def towns(data: tuple = None):
    if data is None:
        data = get_data()
    rdata, tdata = data[0], data[1]
    for y in tdata["sets"]["townyPlugin.markerset"]["areas"]:
        if y.endswith("__0"):
            yield Town(y[:-3], data)


class TownNotFound(Exception):
    pass


class Town:
    def __init__(self, name: str, data: tuple = None, nation=None):
        if data is None:
            data = get_data()
        rdata, tdata = data[0], data[1]
        try:
            t = tdata["sets"]["townyPlugin.markerset"]["areas"][name + "__0"]
        except KeyError:
            raise TownNotFound("the town {} was not found".format(name))
        desc = re.sub("<[^>]+>", "||", t["desc"])
        desc = desc.split("||")
        for i, v in enumerate(desc):
            if v == "":
                del desc[i]
        try:
            if nation:
                self.nation = nation
            else:
                self.nation = Nation(desc[1][:-1].split("(")[1], data)
        except NationNotFound:
            self.nationless = True
        else:
            self.nationless = False
        self.residents = []
        for x in desc[5].split(", "):
            self.residents.append(Resident(x, data, self))
        self.name = name
        self.mayor = Resident(desc[3], data, self)
        self.pvp = bool(desc[8][5:])
        self.mobSpawns = bool(desc[9][6:])
        self.explosions = bool(desc[11][11:])
        self.fire = bool(desc[12][6:])
        self.capital = bool(desc[13][9:])
        # TODO add position
        # TODO add size


class NationNotFound(Exception):
    pass


class Nation:
    def __init__(self, name: str, data: tuple = None):
        if data is None:
            data = get_data()
        rdata, tdata = data[0], data[1]
        t = tdata["sets"]["townyPlugin.markerset"]["areas"]
        self.towns = []
        for x in t:
            if x.endswith("__0"):
                desc = re.sub("<[^>]+>", "||", t[x]["desc"])
                desc = desc.split("||")
                for i, v in enumerate(desc):
                    if v == "":
                        del desc[i]
                if x.endswith("__0") and name == desc[1][:-1].split("(")[1]:
                    a = Town(x[:-3], data, self)
                    self.towns.append(a)
                    if a.capital:
                        self.mapColor = t[x]["fillcolor"]
                        self.capital = a
                        self.leader = a.mayor
        try:
            self.capital
        except AttributeError:
            raise NationNotFound("the nation {} was not found".format(name))
        self.residents = []
        for x in self.towns:
            for y in x.residents:
                self.residents.append(y)
        self.name = name
        # TODO add position
        # TODO add size
