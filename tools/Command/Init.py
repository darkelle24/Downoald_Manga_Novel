from tools.Load.loadAllSite import loadAllSite
from tools.Load.loadAllManga import loadAllManga
from tools.Load.loadUpdate import loadUpdate
import os

def init(directory: str):
    os.system('color')
    sites = loadAllSite()
    mangas = loadAllManga(directory)
    updates = loadUpdate(directory, sites)

    return (sites, mangas, updates)