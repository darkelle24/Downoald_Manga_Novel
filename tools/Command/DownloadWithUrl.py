from tools.Other.findSiteWithUrl import findSiteWithUrl
from include.Site import Site
from typing import List
from include.Manga import Manga

def downloadWithUrl(opts: List[str], directory: str, sites: List[Site], mangas: List[Manga]):
    url = ""

    for opt in opts:
        if (opt.startswith("http")):
            url = opt
            break
    site = findSiteWithUrl(url, sites)
    if (site != None):
        site.__urlManager__(url, opts, mangas, directory)