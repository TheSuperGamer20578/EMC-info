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
    try:
        data = (
            json.loads(urllib.request.urlopen(
                urllib.request.Request(url="https://earthmc.net/map/up/world/earth/", headers={
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'})).read().decode()),
            json.loads(urllib.request.urlopen(
                urllib.request.Request(url="https://earthmc.net/map/tiles/_markers_/marker_earth.json", headers={
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'})).read().decode()))
        # t = {}
        # for x in [i[:-3] for i in tdata["sets"]["townyPlugin.markerset"]["areas"] if i.endswith("__0")]:
        #     td = tdata["sets"]["townyPlugin.markerset"]["areas"][x+"__0"]
        #     desc = [v for v in re.split(r"<[^<>]*>", td["desc"]) if v != ""]
        #     t[x] = td
        return data
    except urllib.error.HTTPError:
        return get_data()


# noinspection PyUnusedLocal
def onlineResidents(data: tuple = None):
    for x in rdata["players"]:
        yield Resident(x["name"], data)


class Resident:
    def __init__(self, name: str, data: tuple = None, town=None):
        if data is None:
            data = get_data()
        rdata, tdata = data
        t = tdata["sets"]["townyPlugin.markerset"]["areas"]
        if town:
            self.town = town
        else:
            for town in [x for x in t if x.endswith("__0")]:
                desc = [v for v in re.split(r"<[^<>]*>", t[town]["desc"]) if v != ""]
                if name in desc[5].split(", "):
                    self.town = Town(desc[1][:-1].split("(")[0].strip(), data)
                    if not self.town.nationless:
                        self.nation = self.town.nation
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
        # self.name = name
        # if town:
        #     self.town = town

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"""
--- {self.name} ---

"""  # TODO finish this


def towns(data: tuple = None):
    if data is None:
        data = get_data()
    rdata, tdata = data
    return [Town(x[:-3], data) for x in tdata["sets"]["townyPlugin.markerset"]["areas"] if x.endswith("__0")]


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
        self.nationless = False
        try:
            if nation:
                self.nation = nation
            else:
                self.nation = Nation(desc[1][:-1].split("(")[1], data)
        except NationNotFound:
            self.nationless = True
        self.residents = []
        for x in desc[5].split(", "):
            self.residents.append(Resident(x, data, self))
        self.name = name
        self.mayor = Resident(desc[3], data, self)
        self.pvp = (desc[8][5:] == "true")
        self.mobSpawns = (desc[9][6:] == "true")
        self.explosions = (desc[11][11:] == "true")
        self.fire = (desc[12][6:] == "true")
        self.capital = (desc[13][9:] == "true")
        # TODO add position
        # TODO add size

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"""
--- {self.name} ---

"""  # TODO finish this


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

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"""
--- {self.name} ---

"""  # TODO finish this
