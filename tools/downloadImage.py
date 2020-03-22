import os
import requests
import imghdr
from tools.getPage import *

def downloadImage(path, url):
    if not (os.path.isfile(path)):
        r = get_an_page(url)
        if (r == None or imghdr.what(None, r.content) == None):
            return False
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as f:
            f.write(r.content)
        return (True)
    else:
        return (None)