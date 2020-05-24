from tools.downloadImage import downloadImage
from tools.SiteMetaData import chapterInfo
from tools.getPage import getAPage
from tools.remove import remove
from include.Manga import Manga
from typing import Tuple, List, Union, Dict
from termcolor import colored
from bs4 import BeautifulSoup
from tqdm import tqdm
from itertools import repeat
from tools.traductionModule import translateModule
from include.Enum import UrlType, MangaType
import concurrent.futures
import os, shutil

def getChapterNbr(elem: List[Tuple[str, int, int, str]]):
    return float(elem[0][2])

class Site:
    url: str
    siteTypeManga: List[MangaType] = []

    def __getInfoManga__(self, url, soup = None)-> Dict[str, str]:
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

    def __getOneChapter__(self, url: str, path: str)-> List[Tuple[str, int, str, str]]:
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

    def __getAllChapter__(self, url: str) -> Union[List[Tuple[str, str]], BeautifulSoup]:
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

    def __removeChapterAlreadyDownloadManga__(self, chapterList:List[Tuple[str, str]], manga:Manga)->List[Tuple[str, str]] :
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

    def __removeChapterAlreadyDownloadNovel__(self, chapterList:List[Tuple[str, str]], manga:Manga)->List[Tuple[str, str]] :
        if (os.path.exists(manga.path)):
            listChapter = os.listdir(manga.path)
            for file in listChapter :
                chapterNbr = file.replace("Chapter ", "")
                for i, oneChapterTuple in enumerate(chapterList):
                    if (oneChapterTuple[1] == chapterNbr):
                        chapterList.pop(i)
                        break
            return chapterList
        else:
            os.makedirs(manga.path, exist_ok=True)
            manga.save()

    def __recupAllImageFromChapterUrl__(self, urlChapterList:List[Tuple[str, str]])-> List[List[Tuple[str, int, str, str]]]:
        urlImages = []
        result = []

        with concurrent.futures.ThreadPoolExecutor() as executor :
            result = [executor.submit(self.__getOneChapter__, oneChapter[0], oneChapter[1]) for oneChapter in urlChapterList]

            for f in tqdm(concurrent.futures.as_completed(result), total=len(result), leave=False, desc= "Retrieving image URLs", unit="ch"):
                urlImages.append(f.result())
        urlImages = sorted(urlImages, key = getChapterNbr)
        return urlImages

    def __downloadOneImage__(self, oneImage: Tuple[str, int, int, str])-> bool:
        returnValue = downloadImage(oneImage[3], oneImage[0])
        return returnValue

    def __progressBarAllInitManga__(self, urlImages: List[List[Tuple[str, int, str, str]]], mangaName: str):
        with tqdm(total=len(urlImages), desc= mangaName, unit="ch", position=0, leave=True) as bar:
            self.__downloadAllImagesThread__(urlImages, bar)

    def __downloadAllImagesThread__(self, urlImages: List[List[Tuple[str, int, str, str]]], bar: tqdm = None):
        errorChapter = []
        with concurrent.futures.ThreadPoolExecutor() as executor :
            for urlImagesOneChapter in urlImages :
                futures_list = [executor.submit(self.__downloadOneImage__, image) for image in urlImagesOneChapter]
                for f in tqdm(concurrent.futures.as_completed(futures_list), total=len(futures_list), leave=False, desc= "    Chapter " + urlImagesOneChapter[0][2], unit="img"):
                    if (f.result() == False):
                        errorChapter.append(urlImagesOneChapter[0][2])
                chapterInfo(len(urlImagesOneChapter), self.url, urlImagesOneChapter[0][3][:urlImagesOneChapter[0][3].rfind("\\")])
                if not (bar is None):
                    bar.update()

    def __progressBarAllInitNovel__(self, urlChapter: List[Tuple[str, str]], mangaName: str, opts: Dict):
        with tqdm(total=len(urlChapter), desc= mangaName, unit="ch", position=0, leave=True) as bar:
            self.__downloadAllNovel__(urlChapter, opts, bar)

    def getTextFromOneChapter(self, soupOneChapter: BeautifulSoup)->str:
        return ""

    def __getSoupFromNovel__(self, urlOneChapter:str)->BeautifulSoup:
        r = getAPage(urlOneChapter)
        if (r == None):
            return None
        soup = BeautifulSoup(r.text, features="html.parser")
        return (soup)

    def __downoaldNovelOneChapter__(self, urlOneChapter:Tuple[str, str], opts: Dict):
        soup = self.__getSoupFromNovel__(urlOneChapter[0])
        if (soup != None):
            text = self.getTextFromOneChapter(soup)
            os.makedirs(os.path.dirname(urlOneChapter[1]), exist_ok=True)
            with open(urlOneChapter[1], "w+", encoding="utf-8") as file:
                if ("trad" in opts):
                    text = opts["trad"][0].translate(text, dest=opts["trad"][1], src="en").text
                file.write(text)

    def __downloadAllNovel__(self, urlChapter: List[Tuple[str, str]], opts: Dict, bar: tqdm = None):
        for urlOneChapter in urlChapter :
            self.__downoaldNovelOneChapter__(urlOneChapter, opts)
            if not (bar is None):
                bar.update()

    def __addPathToChpterList__(self, urlChapterList:List[Tuple[str, str]], manga: Manga, mangatype: MangaType)->List[Tuple[str, str]]:
        for index, oneChapter in enumerate(urlChapterList):
            if (mangatype == MangaType.MANGA):
                urlChapterList[index] = (oneChapter[0], os.path.join(manga.path, "Manga", "Chapter " + remove(oneChapter[1].strip() ,'\/:*?"<>|')))
            elif (mangatype == MangaType.NOVEL):
                urlChapterList[index] = (oneChapter[0], os.path.join(manga.path, "Novel", "Chapter " + remove(oneChapter[1].strip() ,'\/:*?"<>|') + ".txt"))
        return urlChapterList

    def __managerDownloader__(self, urlChapterList:List[Tuple[str, str]], mangas:List[Manga], urlInfo:str, opts: Dict, mangatype: MangaType, soupInfo:BeautifulSoup = None):
        manga = None
        urlImages = []

        info = self.__getInfoManga__(urlInfo, soupInfo)
        correctNamePath = remove(info["name"].strip() ,'\/:*?"<>|')
        found = [x for x in mangas if x.name == info["name"]]
        if (found == []):
            path = os.path.join(".\\manga", correctNamePath)
            os.makedirs(path, exist_ok=True)
            manga = Manga(info["name"], path, 0, [(self.url, urlInfo)])
            manga.save()
            mangas.append(manga)
        elif (len(found) == 1):
            if (mangatype == MangaType.MANGA):
                urlChapterList = self.__removeChapterAlreadyDownloadManga__(urlChapterList, found[0])
            elif (mangatype == MangaType.NOVEL):
                urlChapterList = self.__removeChapterAlreadyDownloadNovel__(urlChapterList, found[0])
            manga = found[0]
            if (manga.checkRegisterSite(self.url) == False):
                manga.sites = manga.sites +  [(self.url, urlInfo)]
        if (urlChapterList != []):
            if (mangatype == MangaType.MANGA):
                self.__managerDownloaderImage__(urlChapterList, manga, opts)
            elif (mangatype == MangaType.NOVEL):
                self.__managerDownloaderText__(urlChapterList, manga, opts)

    def __managerDownloaderText__(self, urlChapterList: List[Tuple[int, str]], manga: Manga, opts: Dict):
        urlChapterList = self.__addPathToChpterList__(urlChapterList, manga, MangaType.NOVEL)
        urlChapterList.reverse()
        self.__progressBarAllInitNovel__(urlChapterList, manga.name, opts)

    def __managerDownloaderImage__(self, urlChapterList: List[Tuple[int, str]], manga: Manga, opts: Dict):
        urlChapterList = self.__addPathToChpterList__(urlChapterList, manga, MangaType.MANGA)
        urlImages = self.__recupAllImageFromChapterUrl__(urlChapterList)
        self.__progressBarAllInitManga__(urlImages, manga.name)

    def getUrlInfoFromChapter(self, urlChapter: str)-> str :
        if (urlChapter[-1] == "/"):
            urlChapter = urlChapter[:-1]
        return urlChapter[:urlChapter.rfind("/")]

    def __getType__(self, opts: List[str])->MangaType:
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

    def __gestOpt__(self, opts: List[str], typeUrl:UrlType, mangatype: MangaType)-> Dict:
        dictio = {}

        dictio = translateModule(dictio, opts, mangatype)
        return (dictio)

    def urlManager(self, url: str, opts: List[str], mangas: List[Manga], directory: str = "") :
        typeUrl = self.analyseURL(url)
        typemanga = self.__getType__(opts)
        urlInfo = url
        soupInfo = None
        urlChapterList = []

        if (typeUrl != UrlType.NONE and typemanga != MangaType.NONE):
            opts = self.__gestOpt__(opts, typeUrl, typemanga)
            if (typeUrl == UrlType.ALLCHAPTER) :
                urlChapterList, soupInfo = self.__getAllChapter__(url)
            elif (typeUrl == UrlType.ONECHAPTER) :
                urlInfo = self.getUrlInfoFromChapter(url)
                urlChapterList = [(url, self.getChapterNbrFromUrl(url))]
            self.__managerDownloader__(urlChapterList, mangas, urlInfo, opts, typemanga, soupInfo)