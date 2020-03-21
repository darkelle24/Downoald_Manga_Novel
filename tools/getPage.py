from termcolor import colored
import requests
from bs4 import BeautifulSoup
import os

def print_error_request(e, url):
    print(colored("\nRequest Error on " + '\''+ url + '\'' + " with error message:\n\t", "red"), e)
    print()

def get_an_page(url):
    try :
        r = requests.get(url)
    except requests.exceptions.RequestException as e:
        print_error_request(e, url)
        return None
    return (BeautifulSoup(r.text, features="html.parser"))