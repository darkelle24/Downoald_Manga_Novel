from typing import List, Tuple, Set, NoReturn
import json
from json import JSONEncoder
import os

class MangaEncoder(JSONEncoder):
        def default(self, obj): # pylint: disable=method-hidden
            return obj.__dict__

class Manga:
    name: str
    path: str
    nbrChapter: int
    sites: List[Tuple[str, str, str]]
    errorDownload: List[Tuple[int, int]]

    def __init__(self, name: str = "", path:str = "", nbrChapter: int = 0, sites: List[Tuple[str, str]] = [], errorDownload: List[Tuple[int, int]] = []):
        self.name = name
        self.path = path
        self.nbrChapter = nbrChapter
        self.sites = sites
        self.errorDownload = errorDownload

    def load(self, path: str)->NoReturn:
        with open(os.path.join(path, ".info.json"), 'r') as jsonFile:
            data = json.load(jsonFile)
            self.name = data["name"]
            self.path = data["path"]
            self.nbrChapter = data["nbrChapter"]
            self.sites = data["sites"]
            self.errorDownload = data["errorDownload"]

    def save(self, path: str=None)->NoReturn:
        if (path == None):
            path = self.path
        with open(os.path.join(path, ".info.json"), 'w+') as jsonFile:
            json.dump(self, jsonFile, indent=4, cls=MangaEncoder)

    def checkRegisterSite(self, site: str)->bool:
        for siteReg in sites:
            if (siteReg[0] == site):
                return True
        return False