import os
import requests
import imghdr
from tools.Other.getPage import getAPage

def downloadImage(path, url):
    if not (os.path.isfile(path)):
        r = getAPage(url)
        if (r == None or imghdr.what(None, r.content) == None):
            return False
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as f:
            f.write(r.content)
        return (True)
    else:
        return (None)