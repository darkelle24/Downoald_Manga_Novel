from typing import List
import os
from include.Manga import Manga

def loadAllManga()->List[Manga]:
    mangas = []
    if (os.path.isdir(r".\manga") == True):
        for file in os.listdir(r".\manga") :
            path = os.path.join(r".\manga", file)
            if (os.path.isfile(os.path.join(path, ".info.json")) == True):
                manga = Manga()
                manga.load(path)
                mangas.append(manga)
    return mangas