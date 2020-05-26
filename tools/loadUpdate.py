import os
import json
from typing import List
from include.Update import Update
from tools.findSiteWithUrl import findSiteWithUrl
from include.Site import Site
from include.Enum import MangaType

def loadUpdate(sites: Site)->List[Update]:
    listUpdate = []

    if (os.path.isfile(r".\manga\.update.json")):
        with open(r".\manga\.update.json", 'r') as jsonFile:
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