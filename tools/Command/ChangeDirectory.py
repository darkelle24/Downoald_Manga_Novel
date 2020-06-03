import os
from typing import List, Tuple
from tools.Load.loadAllManga import loadAllManga
from tools.Load.loadUpdate import loadUpdate
from include.Site import Site
from include.Manga import Manga
from include.Update import Update

def changeDirectory(sites: List[Site], mangas: List[Manga], updates: List[Update], directory: str, opts: List[str]) ->Tuple[List[Manga], List[Update], str]:
    if (os.path.isdir(opts[1]) == True):
        directory = opts[1]
        mangas = loadAllManga(directory)
        updates = loadUpdate(directory, sites)
    else:
        print("\t" + "Wrong path")
    return mangas, updates, directory