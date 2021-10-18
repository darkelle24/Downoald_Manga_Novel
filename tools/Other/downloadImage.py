import imghdr
import os

import requests

from tools.Other.getPage import getAPage


def downloadImage(path, url)->bool:
    if not (os.path.isfile(path)):
        r = getAPage(url, False, True)
        if (r == None or imghdr.what(None, r.content) == None):
            return False
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as f:
            f.write(r.content)
        return (True)
    else:
        return (None)
