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
        while (getInput.lower() != "stop"):
            getInput = input(">>> ")
            if (getInput.startswith("http")) :
                downloadWithUrl(getInput, directory, sites, mangas)
            elif (getInput.lower() == "site"):
                for site in sites:
                    print(site.url)
            elif (getInput.lower() == "manga"):
                for manga in mangas:
                    print(manga.name)
    except KeyboardInterrupt:
        exit(0)

main()