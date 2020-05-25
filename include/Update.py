from tools.findSiteWithUrl import findSiteWithUrl
from include.Enum import UrlType
from tools.remove import remove

def setUpdateWithUrl(opts, directory, sites, mangas, update)->List[Update]:
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
            update.append(Update(url, float(urlChapterList[-1][1])))
        else:
            print("Wrong type of URL")
    return update

class Update:
    url: str
    last_chapter: float

    def __init__(self, url: str, last_chapter: float):
        self.url = url
        self.last_chapter = last_chapter