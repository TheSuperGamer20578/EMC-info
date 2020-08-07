import json, urllib.request, re


def towns():
    x = json.loads(urllib.request.urlopen(
        urllib.request.Request(url="https://earthmc.net/map/tiles/_markers_/marker_earth.json", headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'})).read().decode())
    for y in x["sets"]["townyPlugin.markerset"]["areas"]:
        if y.endswith("__0"):
            yield Town(y[:-3], x)


class TownNotFoundError(Exception):
    pass


class Town:
    def __init__(self, name: str, data=None):
        if data is None:
            try:
                while data is None:
                    data = json.loads(urllib.request.urlopen(
                        urllib.request.Request(url="https://earthmc.net/map/tiles/_markers_/marker_earth.json", headers={
                            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'})).read().decode())
            except urllib.error.HTTPError:
                pass
        try:
            t = data["sets"]["townyPlugin.markerset"]["areas"][name+"__0"]
        except KeyError:
            raise TownNotFoundError("the town {} was not found".format(name))
        desc = re.sub("<[^>]+>", "||", t["desc"])
        desc = desc.split("||")
        for i,v in enumerate(desc):
            if v == "":
                del desc[i]
        self.mapColor = t["fillcolor"]
        self.name = name
        self.nation = NotImplemented
        self.residents = NotImplemented
        self.mayor = NotImplemented
        self.pvp = bool(desc[8][5:])
        self.mobSpawns = bool(desc[9][6:])
        self.explosions = bool(desc[11][11:])
        self.fire = bool(desc[12][6:])
        self.capital = bool(desc[13][9:])
