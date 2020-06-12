import os
from typing import List, Tuple

from include.Manga import Manga
from include.Site import Site
from include.Update import Update
from tools.Load.loadAllManga import loadAllManga
from tools.Load.loadUpdate import loadUpdate


def changeDirectory(sites: List[Site], mangas: List[Manga], updates: List[Update], directory: str, opts: List[str]) ->Tuple[List[Manga], List[Update], str]:
    directory_temp = ""

    if (len(opts) == 2):
        if (os.path.isabs(opts[1]) == True):
            directory_temp = opts[1]
        else:
            directory_temp = os.path.join(directory, opts[1])
        if (os.path.isdir(directory_temp) == True):
            directory = directory_temp
            mangas = loadAllManga(directory)
            updates = loadUpdate(directory, sites)
        else:
            print("\t" + "Wrong path")
    elif (len(opts) == 1):
        print("\t" + os.path.abspath(directory))
    return mangas, updates, directory
