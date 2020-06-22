from typing import List

from include.Site import Site


def findSiteWithUrl(url: str, sites: List[Site])->Site:
    splited = url.split("/")

    if (len(splited) >= 2):
        for site in sites:
            if (splited[2] == site.url):
                return site
    else:
        print("This url is not an valid url")
        return None
    print("This site is not implemented")
    return None
