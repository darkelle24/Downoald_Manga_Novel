#!/usr/bin/python3

from sys import exit
import os
from include.Site import Site
from tools.loadAllSite import loadAllSite
from tools.loadAllManga import loadAllManga

def downloadWithUrl(url, directory, sites, mangas):
    for site in sites:
        if (url.split("/")[2] == site.url):
            site.urlManager(url, mangas, directory)
            break

def main():
    getInput = ""
    directory = ""
    sites = []
    mangas = []

    os.system('color')
    sites = loadAllSite()
    mangas = loadAllManga()
    try:
        while (getInput != "STOP"):
            getInput = input(">>> ")
            if (getInput.startswith("http")) :
                downloadWithUrl(getInput, directory, sites, mangas)
            elif (getInput == "Site"):
                for site in sites:
                    print(site.url)
    except KeyboardInterrupt:
        exit(0)

main()