#!/usr/bin/python3

from sys import exit
import os
from include.Site import Site
from tools.loadAllSite import loadAllSite
from tools.loadAllManga import loadAllManga
from tools.loadUpdate import loadUpdate
from include.Update import setUpdateWithUrl
from tools.findSiteWithUrl import findSiteWithUrl

def downloadWithUrl(opts, directory, sites, mangas):
    url = ""

    for opt in opts:
        if (opt.startswith("http")):
            url = opt
            break
    site = findSiteWithUrl(url, sites)
    if (site != None):
        site.urlManager(url, opts, mangas, directory)

##def command(cmd: str):
##    switcher={
##            0:zero,
##            1:one,
##            2:lambda:'two'
##            }
##    func = switcher.get(cmd,lambda :'Invalid')
##    return func()

def main():
    getInput = []
    directory = ""
    sites = []
    mangas = []
    updates = []

    os.system('color')
    sites = loadAllSite()
    mangas = loadAllManga()
    updates = loadUpdate()
    try:
        while (getInput == [] or getInput[0].lower() != "stop"):
            getInput = input(">>> ").split(" ")
            getInput[0] = getInput[0].lower()
            if (getInput[0] == "download") :
                downloadWithUrl(getInput, directory, sites, mangas)
            elif (getInput[0] == "site"):
                for site in sites:
                    print("\t" + site.url)
            elif (getInput[0] == "manga"):
                for manga in mangas:
                    print("\t" + manga.name)
            elif (getInput[0] == "help"):
                pass
            elif (getInput[0] == "setupdate"):
                update = setUpdateWithUrl(getInput, directory, sites, mangas, updates)
            elif (getInput[0] == "updatelist"):
                for update in updates:
                    print("\t" + update.url + "  " + update.path + "  " + str(update.last_chapter))
    except KeyboardInterrupt:
        exit(0)

main()