import os

from include.Enum import MangaType
from Site.isekaiscan import isekaiscan
from Site.wuxiaworld import wuxiaworld
from tools.Other.checkModuleExist import module_exists
from tools.Other.downloadImage import downloadImage
from tools.Other.findSiteWithUrl import findSiteWithUrl
from tools.Other.getPage import getAPage


def test__gestOpt__():
    site = isekaiscan()
    assert (site.__gestOpt__(["--workers="])["workers"] == 5)
    assert (site.__gestOpt__(["--workers=10"])["workers"] == 10)
    assert ("notification" in site.__gestOpt__(["--notification"]))
    assert ("notification" in site.__gestOpt__(["-N"]))
    assert ("trad" not in site.__gestOpt__(["-t"], mangatype=MangaType.MANGA))
    assert ("trad" not in site.__gestOpt__(["--trad=fr"], mangatype=MangaType.MANGA))

    assert ("trad" in site.__gestOpt__(["-t"], mangatype=MangaType.NOVEL))
    assert ("trad" in site.__gestOpt__(["--trad=fr"], mangatype=MangaType.NOVEL))

def test__getType__():
    site = isekaiscan()
    assert (site.__getType__() == MangaType.MANGA)
    assert (site.__getType__(["-n"]) == MangaType.NONE)
    assert (site.__getType__(["--novel"]) == MangaType.NONE)
    assert (site.__getType__(["-m"]) == MangaType.MANGA)
    assert (site.__getType__(["--manga"]) == MangaType.MANGA)

    site = wuxiaworld()
    assert (site.__getType__() == MangaType.NOVEL)
    assert (site.__getType__(["-n"]) == MangaType.NOVEL)
    assert (site.__getType__(["--novel"]) == MangaType.NOVEL)
    assert (site.__getType__(["-m"]) == MangaType.NONE)
    assert (site.__getType__(["--manga"]) == MangaType.NONE)

def test__getInfoManga__():
    site = isekaiscan()
    info = site.__getInfoManga__("dab")
    assert(info == None)

    info = site.__getInfoManga__("https://isekaiscan.com/manga/i-am-the-sorcerer-king/")
    assert(info["name"] == "I Am The Sorcerer King")

    site = wuxiaworld()
    info = site.__getInfoManga__("dab")
    assert(info == None)

    info = site.__getInfoManga__("https://wuxiaworld.site/novel/the-legendary-mechanic/")
    assert(info["name"] == 'The Legendary Mechanic')

def test_getAPage():
    assert (getAPage("dab", True) == None)
    assert (getAPage("https://wuxiaworld.site/novel/the-legendary-mechanic/", True) != None)

def test_findSiteWithUrl():
    sites = [isekaiscan(), wuxiaworld()]
    assert (findSiteWithUrl("qdqd", sites) == None)
    assert (findSiteWithUrl("https://wuxiaworld.site/novel/the-legendary-mechanic/", sites) == sites[1])
    assert (findSiteWithUrl("https://isekaiscan.com/manga/the-scholars-reincarnation/", sites) == sites[0])

def test_module_exists():
    assert(module_exists("qdqdqd") == False)
    assert(module_exists("pip") == True)

def test_downloadImage():
    assert(downloadImage("TU.py", "") == None)
    assert(downloadImage("./UWU.jpg", "qdqdqdq") == False)
    assert(downloadImage("./UWU.jpg", "https://m.media-amazon.com/images/I/4141ztFVb3L._SS500_.jpg") == True)
    os.remove("./UWU.jpg")

test_downloadImage()
test_module_exists()
test_findSiteWithUrl()
test_getAPage()
test__getInfoManga__()
test__getType__()
test__gestOpt__()
