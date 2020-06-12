from typing import List

from include.Site import Site


def findSiteWithUrl(url: str, sites: List[Site])->Site:
    for site in sites:
        if (url.split("/")[2] == site.url):
            return site
    print("This site is not implemented")
    return None
