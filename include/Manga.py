import json
import os
from json import JSONEncoder
from typing import List, NoReturn, Set, Tuple


class MangaEncoder(JSONEncoder):
        def default(self, obj): # pylint: disable=method-hidden
            return obj.__dict__

class Manga:
    name: str
    path: str
    pathImage: str
    nbrChapterManga: int
    nbrChapterNovel: int
    sites: List[Tuple[str, str, str]]
    errorDownload: List[Tuple[int, int]]

    def __init__(self, name: str = "", path:str = "", sites: List[Tuple[str, str]] = [], errorDownload: List[Tuple[int, int]] = [], pathImage: str = ""):
        self.name = name
        self.path = path
        self.sites = sites
        self.errorDownload = errorDownload
        self.nbrChapterManga = 0
        self.nbrChapterNovel = 0
        self.pathImage = pathImage
        self.refresh()

    def refresh(self):
        self.countChapterManga()
        self.countChapterNovel()

    def countChapterManga(self):
        path = os.path.join(self.path, "Manga")
        self.nbrChapterManga = 0

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
        self.nbrChapterNovel = 0

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
            self.errorDownload = data.get("errorDownload", [])
            self.pathImage = data.get("pathImage", "")
            if (self.pathImage != "" and os.path.isfile(self.pathImage) == False):
                self.pathImage = ""
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
