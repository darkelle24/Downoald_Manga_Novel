import os

from tools.Load.loadAllManga import loadAllManga
from tools.Load.loadAllSite import loadAllSite
from tools.Load.loadUpdate import loadUpdate


def init(directory: str = "./manga"):
    os.system('color')
    sites = loadAllSite()
    mangas = loadAllManga(directory)
    updates = loadUpdate(directory, sites)

    return (sites, mangas, updates)
