from termcolor import colored
import requests
from bs4 import BeautifulSoup
import os

def print_error_request(e, url):
    print(colored("\nRequest Error on " + '\''+ url + '\'' + " with error message:\n\t", "red"), e)
    print()

def getAPage(url):
    try :
        r = requests.get(url)
    except requests.exceptions.RequestException:
        ##print_error_request(e, url)
        return None
    if (r.status_code != 200):
        return None
    return (r)