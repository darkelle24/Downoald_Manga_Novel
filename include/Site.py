from tools.downloadImage import downloadImage
from tools.SiteMetaData import chapterInfo
from tools.getPage import getAPage
from include.Manga import Manga
from typing import Tuple, List, Union, Dict
from termcolor import colored
from bs4 import BeautifulSoup
from enum import Enum
from tqdm import tqdm
from itertools import repeat
import concurrent.futures
import os, shutil

class UrlType(Enum):
    ALLCHAPTER = 1
    ONECHAPTER = 2
    NONE = -1

class MangaType(Enum):
    NOVEL = 1
    MANGA = 2
    NONE = -1

def getChapterNbr(elem: List[Tuple[str, int, int, str]]):
    return float(elem[0][2])

class Site:
    url: str
    siteTypeManga: List[MangaType] = []

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

    def getOneChapter(self, url: str, path: str)-> List[Tuple[str, int, str, str]]:
        imageList: List[Tuple[str, int, str]]

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

    def recupAllChapter(self, soup: BeautifulSoup) -> List[Tuple[str, str]]:
        return []

    def analyseURL(self, url:str)->UrlType :
        return UrlType.NONE

    def getChapterNbrFromUrl(self, urlChapter: str)-> str:
        return urlChapter

    def removeChapterAlreadyDownload(self, chapterList:List[Tuple[str, str]], manga:Manga)->List[Tuple[int, str]] :
        if (os.path.exists(manga.path)):
            listChapter = os.listdir(manga.path)
            for file in listChapter :
                chapterNbr = file.replace("Chapter ", "")
                if (file != ".info.json" and os.path.isfile(os.path.join(manga.path, file, ".info.json")) == True):
                    for i, oneChapterTuple in enumerate(chapterList):
                        if (oneChapterTuple[1] == chapterNbr):
                            chapterList.pop(i)
                            break
                elif (file != ".info.json"):
                    shutil.rmtree(os.path.join(manga.path, file))
            return chapterList
        else:
            os.makedirs(manga.path, exist_ok=True)
            manga.save()

    def recupAllImageFromChapterUrl(self, urlChapterList:List[Tuple[str, str]])-> List[List[Tuple[str, int, str, str]]]:
        urlImages = []
        result = []

        with concurrent.futures.ThreadPoolExecutor() as executor :
            result = [executor.submit(self.getOneChapter, oneChapter[0], oneChapter[1]) for oneChapter in urlChapterList]

            for f in tqdm(concurrent.futures.as_completed(result), total=len(result), leave=False, desc= "Retrieving image URLs", unit="ch"):
                urlImages.append(f.result())
        urlImages = sorted(urlImages, key = getChapterNbr)
        return urlImages

    def downloadOneImage(self, oneImage: Tuple[str, int, int, str])-> bool:
        returnValue = downloadImage(oneImage[3], oneImage[0])
        return returnValue

    def progress_bar_all_init(self, urlImages: List[List[Tuple[str, int, str, str]]], mangaName: str)->List[str]:
        with tqdm(total=len(urlImages), desc= mangaName, unit="ch", position=0, leave=True) as bar:
            self.downloadAllImagesThread(urlImages, bar)

    def downloadAllImagesThread(self, urlImages: List[List[Tuple[str, int, str, str]]], bar: tqdm = None) -> List[str]:
        errorChapter = []
        with concurrent.futures.ThreadPoolExecutor() as executor :
            for urlImagesOneChapter in urlImages :
                futures_list = [executor.submit(self.downloadOneImage, image) for image in urlImagesOneChapter]
                for f in tqdm(concurrent.futures.as_completed(futures_list), total=len(futures_list), leave=False, desc= "    Chapter " + urlImagesOneChapter[0][2], unit="img"):
                    if (f.result() == False):
                        errorChapter.append(urlImagesOneChapter[0][2])
                chapterInfo(len(urlImagesOneChapter), self.url, urlImagesOneChapter[0][3][:urlImagesOneChapter[0][3].rfind("\\")])
                if not (bar is None):
                    bar.update()

    def addPathToChpterList(self, urlChapterList:List[Tuple[str, str]], manga: Manga, mangatype: MangaType)->List[Tuple[str, str]]:
        for index, oneChapter in enumerate(urlChapterList):
            if (mangatype == MangaType.MANGA):
                urlChapterList[index] = (oneChapter[0], os.path.join(manga.path, "Manga", "Chapter " + oneChapter[1].strip()))
            elif (mangatype == MangaType.NOVEL):
                urlChapterList[index] = (oneChapter[0], os.path.join(manga.path, "Novel", "Chapter " + oneChapter[1].strip()))
        return urlChapterList

    def managerDownloader(self, urlChapterList:List[Tuple[str, str]], mangas:List[Manga], urlInfo:str, opts: List[str], mangatype: MangaType, soupInfo:BeautifulSoup = None):
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
        if (urlChapterList != []):
            if (mangatype == MangaType.MANGA):
                self.managerDownloaderImage(urlChapterList, manga)
            elif (mangatype == MangaType.NOVEL):
                pass

    def managerDownloaderImage(self, urlChapterList: List[Tuple[int, str]], manga: Manga):
        urlChapterList = self.addPathToChpterList(urlChapterList, manga, MangaType.MANGA)
        urlImages = self.recupAllImageFromChapterUrl(urlChapterList)
        self.progress_bar_all_init(urlImages, manga.name)

    def getUrlInfoFromChapter(self, urlChapter: str)-> str :
        if (urlChapter[-1] == "/"):
            urlChapter = urlChapter[:-1]
        return urlChapter[:urlChapter.rfind("/")]

    def getType(self, opts: List[str])->MangaType:
        if (self.siteTypeManga != []):
            for opt in opts:
                if (opt == '-m' or opt == "--manga"):
                    if (MangaType.MANGA in self.siteTypeManga):
                        return MangaType.MANGA
                    else:
                        print("This site doesn’t accept this type of manga")
                        return MangaType.NONE
                if (opt == '-n' or opt == "--novel"):
                    if (MangaType.NOVEL in self.siteTypeManga):
                        return MangaType.NOVEL
                    else:
                        print("This site doesn’t accept this type of manga")
                        return MangaType.NONE
            return MangaType.MANGA
        else:
            print("This site doesn’t have any type of manga")
            return MangaType.NONE

    def urlManager(self, url: str, opts: List[str], mangas: List[Manga], directory: str = "") :
        typeUrl = self.analyseURL(url)
        typemanga = self.getType(opts)
        urlInfo = url
        soupInfo = None
        urlChapterList = []

        if (typeUrl != UrlType.NONE and typemanga != MangaType.NONE):
            if (typeUrl == UrlType.ALLCHAPTER) :
               urlChapterList, soupInfo = self.getAllChapter(url)
            elif (typeUrl == UrlType.ONECHAPTER) :
                urlInfo = self.getUrlInfoFromChapter(url)
                urlChapterList = (url, self.getChapterNbrFromUrl(url))
            self.managerDownloader(urlChapterList, mangas, urlInfo, opts, typemanga, soupInfo)