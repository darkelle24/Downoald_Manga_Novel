from enum import Enum

class UrlType(Enum):
    ALLCHAPTER = 1
    ONECHAPTER = 2
    NONE = -1

class MangaType(int, Enum):
    NOVEL = 1
    MANGA = 2
    NONE = -1