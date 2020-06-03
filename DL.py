#!/usr/bin/python3

from sys import exit
import os
from include.Site import Site
from tools.Load.loadAllSite import loadAllSite
from tools.Load.loadAllManga import loadAllManga
from tools.Load.loadUpdate import loadUpdate
from include.Update import setUpdateWithUrl, getUpdate
from tools.Other.findSiteWithUrl import findSiteWithUrl
import sys

def downloadWithUrl(opts, directory, sites, mangas):
    url = ""

    for opt in opts:
        if (opt.startswith("http")):
            url = opt
            break
    site = findSiteWithUrl(url, sites)
    if (site != None):
        site.__urlManager__(url, opts, mangas, directory)

##def command(cmd: str):
##    switcher={
##            0:zero,
##            1:one,
##            2:lambda:'two'
##            }
##    func = switcher.get(cmd,lambda :'Invalid')
##    return func()

def init():
    os.system('color')
    sites = loadAllSite()
    mangas = loadAllManga()
    updates = loadUpdate(sites)

    return (sites, mangas, updates)

def main():
    getInput = []
    directory = ""
    sites = []
    mangas = []
    updates = []

    sites, mangas, updates = init()
    try:
        while (getInput == [] or getInput[0].lower() != "stop"):
            ##try:
                getInput = input(">>> ").strip().split(" ")
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
                    updates = setUpdateWithUrl(getInput, sites, updates)
                elif (getInput[0] == "updatelist"):
                    for update in updates:
                        print("\t" + update.__str__())
                elif (getInput[0] == "update"):
                    getUpdate(getInput, updates, mangas)
                elif (getInput[0] == "reload"):
                    directory = ""
                    sites, mangas, updates = init()
            ##except:
            ##    print("Unexpected error: ", sys.exc_info()[0], file=sys.stderr)
    except KeyboardInterrupt:
        exit(0)

if (__name__== "__main__"):
    main()