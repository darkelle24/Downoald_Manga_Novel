import os
import json
from typing import List
from include.Update import Update
from tools.Other.findSiteWithUrl import findSiteWithUrl
from include.Site import Site
from include.Enum import MangaType

def loadUpdate(directory: str, sites: Site)->List[Update]:
    listUpdate = []
    path = os.path.join(directory, ".update.json")

    if (os.path.isfile(path)):
        with open(path, 'r') as jsonFile:
            data = json.load(jsonFile)
            for update in data:
                url = update["url"]
                last_chapter = update["last_chapter"]
                mangaType = update["mangaType"]
                if (url != None and last_chapter != None and mangaType != None and mangaType != MangaType.NONE):
                    site = findSiteWithUrl(url, sites)
                    if (site != None):
                        listUpdate.append(Update(url, site, last_chapter, mangaType))
    return listUpdate