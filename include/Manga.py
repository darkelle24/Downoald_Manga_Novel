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
    nbrChapterManga: int
    nbrChapterNovel: int
    sites: List[Tuple[str, str, str]]
    errorDownload: List[Tuple[int, int]]

    def __init__(self, name: str = "", path:str = "", sites: List[Tuple[str, str]] = [], errorDownload: List[Tuple[int, int]] = []):
        self.name = name
        self.path = path
        self.sites = sites
        self.errorDownload = errorDownload
        self.refresh()

    def refresh(self):
        self.countChapterManga()
        self.countChapterNovel()

    def countChapterManga(self):
        path = os.path.join(self.path, "Manga")

        if (os.path.isdir(path)):
            listChapter = os.listdir(path)
            for file in listChapter :
                if (file != ".info.json" and file.startswith("Chapter") and os.path.isdir(os.path.join(path, file)) == True
                    and os.path.isfile(os.path.join(path, file, ".info.json")) == True):
                    self.nbrChapterManga += 1
        else:
            self.nbrChapterManga = 0

    def countChapterNovel(self):
        path = os.path.join(self.path, "Novel")

        if (os.path.isdir(path)):
            listChapter = os.listdir(path)
            for file in listChapter :
                if (file != ".info.json" and file.startswith("Chapter") and os.path.isfile(os.path.join(path, file)) == True):
                    self.nbrChapterNovel += 1
        else:
            self.nbrChapterNovel = 0

    def load(self, path: str)->NoReturn:
        with open(os.path.join(path, ".info.json"), 'r') as jsonFile:
            data = json.load(jsonFile)
            self.name = data["name"]
            self.path = data["path"]
            self.sites = data["sites"]
            self.errorDownload = data["errorDownload"]
            self.refresh()

    def save(self, path: str=None)->NoReturn:
        if (path == None):
            path = self.path
        with open(os.path.join(path, ".info.json"), 'w+') as jsonFile:
            json.dump(self, jsonFile, indent=4, cls=MangaEncoder)

    def checkRegisterSite(self, site: str)->bool:
        for siteReg in self.sites:
            if (siteReg[0] == site):
                return True
        return False