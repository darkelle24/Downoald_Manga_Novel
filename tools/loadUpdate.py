import os
import json
from typing import List
from include.Update import Update

def loadUpdate()->List[Update]:
    listUpdate = []

    if (os.path.isfile(r".\manga\.update.json")):
        with open(r".\manga\.update.json", 'r') as jsonFile:
            data = json.load(jsonFile)
            for update in data:
                url = update["url"]
                last_chapter = update["last_chapter"]
                if (url != None and last_chapter != None):
                    listUpdate.append(Update(url, last_chapter))
    return listUpdate