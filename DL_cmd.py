#!/usr/bin/python3

from sys import exit
from tools.Command.DownloadWithUrl import downloadWithUrl
from tools.Command.Init import init
from tools.Command.ChangeDirectory import changeDirectory
from include.Update import setUpdateWithUrl, getUpdate
import sys

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
    directory = "./manga"
    sites = []
    mangas = []
    updates = []

    sites, mangas, updates = init(directory)
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
                    sites, mangas, updates = init(directory)
                elif (getInput[0] == "directory"):
                    mangas, updates, directory = changeDirectory(sites, mangas, updates, directory, getInput)
            ##except:
            ##    print("Unexpected error: ", sys.exc_info()[0], file=sys.stderr)
    except KeyboardInterrupt:
        exit(0)

if (__name__== "__main__"):
    main()