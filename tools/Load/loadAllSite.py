import os
from typing import List

from include.Site import Site


def loadAllSite()->List[Site]:
    sites = []
    for file in os.listdir(r".\Site") :
        if (file.endswith(".py")):
            siteName = os.path.splitext(file)[0]
            mod = __import__("Site." + siteName, fromlist=[siteName])
            site = getattr(mod, siteName)
            sites.append(site())
    return sites
