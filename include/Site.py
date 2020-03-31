from tools.downloadImage import downloadImage
from tools.SiteMetaData import chapterMetaData
from tools.getPage import getAPage
from include.Manga import Manga
from typing import Tuple, List, Union, Dict
from termcolor import colored
from bs4 import BeautifulSoup
from enum import Enum
import concurrent.futures
import os

class UrlType(Enum):
    ALLCHAPTER = 1
    ONECHAPTER = 2
    NONE = -1

def getChapterNbr(elem: List[Tuple[str, int, int, str]]):
    return float(elem[0][2])

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

    def getOneChapter(self, url: str, path: str)-> List[Tuple[str, int, int, str]]:
        imageList: List[Tuple[str, int, int]]

        r = getAPage(url)
        if (r == None):
            print(colored(("Problem Page for this URL: " + url, "red")))
            return (None)
        soup = BeautifulSoup(r.text, features="html.parser")
        imageList = self.recupOneChapter(soup, path)
        return imageList

    def recupOneChapter(self, soup: BeautifulSoup, path: str)->List[Tuple[str, int, int, str]]:
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

    def analyseURL(self, url:str)->UrlType :
        return UrlType.NONE

    def getChapterNbrFromUrl(self, urlChapter: str)-> str:
        return urlChapter

    def removeChapterAlreadyDownload(self, chapterList:List[Tuple[str, str]], manga:Manga)->List[Tuple[int, str]] :
        if (os.path.exists(manga.path)):
            for file in os.listdir(manga.path) :
                chapterNbr = file.replace("Chapter ", "")
                for i, oneChapterTuple in enumerate(chapterList):
                    if (oneChapterTuple[1] == chapterNbr):
                        chapterList.pop(i)
                        break
            return chapterList
        else:
            os.makedirs(manga.path, exist_ok=True)
            manga.save()

    def recupAllImageFromChapterUrl(self, urlChapterList:List[Tuple[str, str]])-> List[List[Tuple[str, int, int, str]]]:
        urlImages = []
        result = []

        with concurrent.futures.ThreadPoolExecutor() as executor :
            result = [executor.submit(self.getOneChapter, oneChapter[0], oneChapter[1]) for oneChapter in urlChapterList]

            for f in concurrent.futures.as_completed(result):
                urlImages.append(f.result())
        urlImages = sorted(urlImages, key = getChapterNbr)
        return urlImages

    def downloadOneImage(self, oneImage: Tuple[str, int, int, str]):
        downloadImage(oneImage[3], oneImage[0])
        ##  if (downloadImage(path, url) == False):
        ##    error_list.append(int(nbr))
        ##chapterMetaData(error_list, directory)

    def downloadAllImagesThread(self, urlImages: List[List[Tuple[str, int, int, str]]]):
        for urlImagesOneChapter in urlImages :
            with concurrent.futures.ThreadPoolExecutor() as executor :
                executor.map(self.downloadOneImage, urlImagesOneChapter)

    def addPathToChpterList(self, urlChapterList:List[Tuple[str, str]], manga: Manga)->List[Tuple[str, str]]:
        for index, oneChapter in enumerate(urlChapterList):
            urlChapterList[index] = (oneChapter[0], os.path.join(manga.path, "Chapter " + oneChapter[1].strip()))
        return urlChapterList

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
        urlChapterList = self.addPathToChpterList(urlChapterList, manga)
        urlImages = self.recupAllImageFromChapterUrl(urlChapterList)
        self.downloadAllImagesThread(urlImages)

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