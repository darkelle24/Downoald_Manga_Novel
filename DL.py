#!/usr/bin/python3

from sys import exit
import os
from Site.ISite import *
from Site.manga.isekaiscan import *

site = {"isekaiscan.com": isekaiscan}

def downoald_with_url(url, directory):
    for name, site_class in site.items():
        if (url.split("/")[2] == name):
            site_class.urlDownload(url=url, directory=directory)
            break

def main():
    getInput = ""
    directory = ""

    os.system('color')
    try:
        directory = input(">>> Path to Directory: ")
        if (directory != "" and (directory[-1] != '\\' or directory[-1] != '/')):
            directory = directory + '\\'
        while (getInput != "STOP"):
            getInput = input(">>> ")
            downoald_with_url(getInput, directory) 
    except KeyboardInterrupt:
        exit(0)

main()