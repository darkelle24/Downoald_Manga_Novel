import os

import requests
from bs4 import BeautifulSoup
from termcolor import cprint


def print_error_request(e, url):
    cprint("\nRequest Error on ", "red", end='')
    cprint('\''+ url + '\'', "white", end="")
    cprint(" with error message:\n\t", "red", end='')
    print(e)

def getAPage(url, printError:bool = False, image: bool = False):
    try :
        if (image):
            r = requests.get(url, stream = True)
        else:
            r = requests.get(url)
    except requests.exceptions.RequestException as msg:
        if (printError == True):
            print_error_request(msg, url)
        return None
    if (r.status_code != 200):
        return None
    return (r)
