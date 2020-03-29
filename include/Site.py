from tools.downloadImage import downloadImage
from tools.SiteMetaData import chapterMetaData
from tools.getPage import getAPage
from include.Manga import Manga
from typing import Tuple, List, Union, Dict
from termcolor import colored
from bs4 import BeautifulSoup
from enum import Enum
import os

class UrlType(Enum):
    ALLCHAPTER = 1
    ONECHAPTER = 2
    NONE = -1

def getChapterNbr(elem: Tuple[str, str]):
    return float(elem[1])

class Site:
    url: str

    def getInfoManga(self, url, soup = None)-> Dict[str, str]:
        info = dict()

        if (soup == None):
            r = getAPage(url)
            if (r == None):
                print(colored(("Problem Info Page", "red")))
                return "ERROR", -1, ("","","")
            soup = BeautifulSoup(r.text, features="html.parser")
        info = self.recupInfoManga(soup, info)
        info["urlSite"] = self.url
        info["urlInfo"] = url
        return (info)

    def recupInfoManga(self, soup: BeautifulSoup, info: Dict[str, str])-> Dict[str, str]:
        return {}

    def getOneChapter(self, url: str)-> List[Tuple[str, int, int]]:
        imageList: List[Tuple[str, int, int]]

        r = getAPage(url)
        if (r == None):
            print(colored(("Problem Page for this URL: " + url, "red")))
            return (None)
        soup = BeautifulSoup(r.text, features="html.parser")
        imageList = self.recupOneChapter(soup)
        return imageList

    def recupOneChapter(self, soup: BeautifulSoup)->List[Tuple[str, int, int]]:
        return []

    def getAllChapter(self, url: str) -> Union[List[Tuple[str, str]], BeautifulSoup]:
        list_chapter = []

        r = getAPage(url)
        if (r == None):
            return None
        soup = BeautifulSoup(r.text, features="html.parser")
        list_chapter = self.recupAllChapter(soup)
        return (list_chapter, soup)
        ##progress_bar_all_chapter(list_chapter, self, directory)

    def recupAllChapter(self, soup: BeautifulSoup) -> List[Tuple[str, str]]:
        return []

    def recupImagePath(self, urlChapterList: List[str]) -> List[Tuple[str, int, int]]:
        imageList = []

        for oneChapterURL in urlChapterList:
            imageList = imageList + self.getOneChapter(oneChapterURL)
        return imageList

    def analyseURL(self, url:str)->UrlType :
        return UrlType.NONE

    def getChapterNbrFromUrl(self, urlChapter: str)-> str:
        return urlChapter

    def removeChapterAlreadyDownload(self, chapterList:List[Tuple[str, str]], manga:Manga)->List[Tuple[int, str]] :
        for file in os.listdir(manga.path) :
            chapterNbr = file.replace("Chapter ", "")
            for i, oneChapterTuple in enumerate(chapterList):
                if (oneChapterTuple[1] == chapterNbr):
                    chapterList.pop(i)
                    break
        return chapterList

    def recupAllImageFromChapterUrl(self, urlChapterList:List[Tuple[str, str]])-> List[Tuple[str, int, int]]:
        urlImages = []

        for oneChapter in urlChapterList:
            urlImages += self.getOneChapter(oneChapter[0])
        return urlImages

    def downloadAllImages(self, urlImages: List[Tuple[str, int, int]], manga: Manga):
        for oneImage in urlImages:
            path = os.path.join(manga.path, "Chapter " + str(oneImage[2]), str(oneImage[1]) + oneImage[0][oneImage[0].rfind("."):])
            downloadImage(path, oneImage[0])
        ##  if (downloadImage(path, url) == False):
        ##    error_list.append(int(nbr))
        ##chapterMetaData(error_list, directory)

    def managerDownloaderImage(self, urlChapterList:List[Tuple[str, str]], mangas:List[Manga], urlInfo:str, soupInfo:BeautifulSoup = None):
        manga = None
        urlImages = []

        info = self.getInfoManga(urlInfo, soupInfo)
        found = [x for x in mangas if x.name == info["name"]]
        if (found == []):
            path = os.path.join(".\\manga", info["name"])
            os.makedirs(path, exist_ok=True)
            manga = Manga(info["name"], path)
            manga.save()
            mangas.append(manga)
        elif (len(found) == 1):
            urlChapterList = self.removeChapterAlreadyDownload(urlChapterList, found[0])
            manga = found[0]
        urlChapterList = sorted(urlChapterList, key = getChapterNbr)
        urlImages = self.recupAllImageFromChapterUrl(urlChapterList)
        self.downloadAllImages(urlImages, manga)

    def getUrlInfoFromChapter(self, urlChapter: str)-> str :
        if (urlChapter[-1] == "/"):
            urlChapter = urlChapter[:-1]
        return urlChapter[:urlChapter.rfind("/")]

    def urlManager(self, url: str, mangas: List[Manga], directory: str = "") :
        typeUrl = self.analyseURL(url)
        urlInfo = url
        soupInfo = None
        urlChapterList = []

        if (typeUrl != UrlType.NONE):
            if (typeUrl == UrlType.ALLCHAPTER) :
               urlChapterList, soupInfo = self.getAllChapter(url)
            elif (typeUrl == UrlType.ONECHAPTER) :
                urlInfo = self.getUrlInfoFromChapter(url)
                urlChapterList = (url, self.getChapterNbrFromUrl(url))
            self.managerDownloaderImage(urlChapterList, mangas, urlInfo, soupInfo)