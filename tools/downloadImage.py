import os
import requests

def downloadImage(path, url):
    if not (os.path.isfile(path)):
        print ("Dont Excist")
        r = requests.get(url)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as f:
            f.write(r.content)
    else:
        print ('Ecxist')