from tools.findSiteWithUrl import findSiteWithUrl
from include.Enum import UrlType
from tools.remove import remove
import json
from typing import List
import os

class Update:
    url: str
    last_chapter: float

    def __init__(self, url: str, last_chapter: float):
        self.url = url
        self.last_chapter = last_chapter

    def __str__(self):
        return (self.url + "  " + str(self.last_chapter))

def obj_dict(obj):
    return obj.__dict__

def saveUpdateList(update):
    with open(r".\manga\.update.json", 'w+') as jsonFile:
        json.dump(update, jsonFile, indent=4, default=obj_dict)

def setUpdateWithUrl(opts, sites, update)->List[Update]:
    url = ""

    for opt in opts:
        if (opt.startswith("http")):
            url = opt
            break
    site = findSiteWithUrl(url, sites)
    if (site != None):
        typeUrl = site.analyseURL(url)
        if (typeUrl == UrlType.ALLCHAPTER):
            urlChapterList, soupInfo = site.__getAllChapter__(url)
            ##info = site.__getInfoManga__(urlInfo, soupInfo)
            ##correctNamePath = remove(info["name"].strip() ,'\/:*?"<>|')
            update.append(Update(url, float(urlChapterList[0][1])))
            saveUpdateList(update)
        else:
            print("Wrong type of URL")
    return update