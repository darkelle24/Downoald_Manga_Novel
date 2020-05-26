from tools.findSiteWithUrl import findSiteWithUrl
from include.Enum import UrlType, MangaType
from tools.remove import remove
from include.Site import Site
from include.Manga import Manga
import json
from typing import List
import os

class Update:
    url: str
    mangaType: MangaType
    last_chapter: float
    site: Site

    def __init__(self, url: str, site: Site, last_chapter: float, mangaType: MangaType):
        self.url = url
        self.last_chapter = last_chapter
        self.site = site
        self.mangaType = mangaType

    def __str__(self):
        return (self.url + "  " + str(self.last_chapter) + "  " + self.site.url + "  " + str(self.mangaType))

    def update(self, mangas: List[Manga]):
        urlChapterList, soupInfo = self.site.__getAllChapter__(self.url)
        urlChapterList = [chapter for chapter in urlChapterList if float(chapter[1]) > self.last_chapter]
        if (urlChapterList != []):
            max = float(urlChapterList[0][1])
            self.site.__managerDownloader__(urlChapterList, mangas, self.url, {}, self.mangaType, soupInfo)
            self.last_chapter = max


def obj_dict(obj):
    return obj.__dict__

def saveUpdateList(update):
    os.makedirs(r".\manga", exist_ok=True)
    with open(r".\manga\.update.json", 'w+') as jsonFile:
        json.dump(update, jsonFile, indent=4, default=obj_dict)

def setUpdateWithUrl(opts, sites, update)->List[Update]:
    url = ""
    mangaType = MangaType.NONE

    for opt in opts:
        if (opt.startswith("http")):
            url = opt
    site = findSiteWithUrl(url, sites)
    if (site != None):
        mangaType = site.__getType__(opts)
        if (mangaType != MangaType.NONE):
            typeUrl = site.analyseURL(url)
            if (typeUrl == UrlType.ALLCHAPTER):
                urlChapterList, soupInfo = site.__getAllChapter__(url)
                ##info = site.__getInfoManga__(urlInfo, soupInfo)
                ##correctNamePath = remove(info["name"].strip() ,'\/:*?"<>|')
                update.append(Update(url, site, float(urlChapterList[0][1]), mangaType))
                saveUpdateList(update)
            else:
                print("Wrong type of URL")
    return update

def getUpdate(updates: List[Update], mangas: List[Manga]):
    for update in updates:
        update.update(mangas)
        saveUpdateList(updates)