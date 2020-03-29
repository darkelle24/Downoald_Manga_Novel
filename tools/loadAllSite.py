from typing import List
import os
from include.Site import Site

def loadAllSite()->List[Site]:
    sites = []
    for file in (os.listdir(r".\Site\manga") + os.listdir(r".\Site\novel")) :
        if (file.endswith(".py")):
            siteName = os.path.splitext(file)[0]
            mod = __import__("Site.manga." + siteName, fromlist=[siteName])
            site = getattr(mod, siteName)
            sites.append(site())
    return sites

