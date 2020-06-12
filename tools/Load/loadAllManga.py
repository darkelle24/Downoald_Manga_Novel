import os
from typing import List

from include.Manga import Manga


def loadAllManga(directory: str)->List[Manga]:
    mangas = []
    if (os.path.isdir(directory) == True):
        for file in os.listdir(directory) :
            path = os.path.join(directory, file)
            if (os.path.isfile(os.path.join(path, ".info.json")) == True):
                manga = Manga()
                manga.load(path)
                mangas.append(manga)
    return mangas
