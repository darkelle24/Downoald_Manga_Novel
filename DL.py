#!/usr/bin/python3

from sys import exit
import os
from include.Site import Site
from tools.loadAllSite import loadAllSite
from tools.loadAllManga import loadAllManga

def downloadWithUrl(opts, directory, sites, mangas):
    url = ""
    good = False

    for opt in opts:
        if (opt.startswith("http")):
            url = opt
            break
    for site in sites:
        if (url.split("/")[2] == site.url):
            site.urlManager(url, opts, mangas, directory)
            good = True
            break
    if (good == False):
        print("This site is not implemented")

def main():
    getInput = []
    directory = ""
    sites = []
    mangas = []

    os.system('color')
    sites = loadAllSite()
    mangas = loadAllManga()
    try:
        while (getInput == [] or getInput[0].lower() != "stop"):
            getInput = input(">>> ").split(" ")
            if (getInput[0].startswith("download")) :
                downloadWithUrl(getInput, directory, sites, mangas)
            elif (getInput[0].lower() == "site"):
                for site in sites:
                    print(site.url)
            elif (getInput[0].lower() == "manga"):
                for manga in mangas:
                    print(manga.name)
            elif (getInput[0].lower() == "help"):
                pass
    except KeyboardInterrupt:
        exit(0)

main()