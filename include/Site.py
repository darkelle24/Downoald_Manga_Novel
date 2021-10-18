import concurrent.futures
import os
import shutil
import sys
from typing import Dict, List, Tuple, Union

from bs4 import BeautifulSoup
from termcolor import colored, cprint
from tqdm import tqdm

from include.Enum import MangaType, UrlType
from include.Manga import Manga
from tools.Opt.MangaOpt.numberWorkerOpt import number_worker
from tools.Opt.NovelOpt.traductionModule import translate, translateModule
from tools.Opt.UpdateOpt.NotificationOpt import basicNotif, notificationOpt
from tools.Other.downloadImage import downloadImage
from tools.Other.getPage import getAPage
from tools.Other.remove import remove
from tools.Other.SiteMetaData import chapterInfo


def __getChapterNbr__(elem: List[Tuple[str, int, int, str]]):
    return float(elem[0][2])

class Site:
    url: str
    siteTypeManga: List[MangaType] = []




    def recupInfoManga(self, soup: BeautifulSoup)-> Dict[str, str]:
        """Retrieve the manga informations. Name is required

        Args:
            soup (BeautifulSoup): Have HTML code of the web page in form of BeautifulSoup

        Returns:
            Dict[str, str]: Return a dictionary containing information about the manga. Name is required
        """
        return {}

    def recupAllChapter(self, soup: BeautifulSoup) -> List[Tuple[str, str]]:
        """Retrieve all chapter from the UrlType.ALLCHAPTER

        Args:
            soup (BeautifulSoup): Have HTML code of the web page in form of BeautifulSoup

        Returns:
            List[Tuple[str, str]]: Returns a tuple list containing the chapter url and the chapter number (+ chapter title, optional)
        """
        return []

    def analyseURL(self, url:str)->UrlType :
        """Lets you know from the url of a page if it is a page with all the chapters (UrlType.ALLCHAPTER) or just a chapter (UrlType.ONECHAPTER)

        Args:
            url (str): URL to analyze

        Returns:
            UrlType: Returns the type of the page either UrlType.ALLCHAPTER or UrlType.ONECHAPTER
        """
        return UrlType.NONE

    def getChapterNbrFromUrl(self, urlChapter: str)-> str:
        """Allows you to know the chapter number from the url

        Args:
            urlChapter (str): URL to analyze

        Returns:
            str: Returns the number of the chapter
        """
        return urlChapter

    def getTextFromOneChapter(self, soupOneChapter: BeautifulSoup)->str:
        """Allows you to recover the text of this chapter of a novel

        Args:
            soupOneChapter (BeautifulSoup): Have HTML code of the web page in form of BeautifulSoup

        Returns:
            str: Return the text of this chapter of the novel
        """
        return ""

    def getImageFromOneChapter(self, soup: BeautifulSoup, path: str)->List[Tuple[str, int, int, str]]:
        """Used to retrieve information from the images in this chapter

        Args:
            soup (BeautifulSoup): Have HTML code of the web page in form of BeautifulSoup
            path (str): Have the path to save the image of this chapter

        Returns:
            List[Tuple[str, int, int, str]]: Returns a tuple list containing information about the images in this chapter [ Url to download the image, Number of this image, Number of this chapter, Path of this image ]
        """
        return []

    def getUrlInfoFromChapter(self, urlChapter: str)-> str :
        """Allows to recover from the URL the URL of the web page containing all the chapters

        Args:
            urlChapter (str): URL to analyze

        Returns:
            str: URL of the web page containing all the chapter
        """
        if (urlChapter[-1] == "/"):
            urlChapter = urlChapter[:-1]
        return urlChapter[:urlChapter.rfind("/")]

    def getMangaImage(self, soup: BeautifulSoup)-> str :
        """Allows to recover the front image of manga/novel (Optionnel)

        Args:
            soup (BeautifulSoup): Have HTML code of the web page in form of BeautifulSoup

        Returns:
            str: URL of the front image
        """
        return ""




    def __getInfoManga__(self, url, soup = None)-> Dict[str, str]:
        if (soup == None):
            r = getAPage(url)
            if (r == None):
                cprint("Problem Info Page", 'red', file=sys.stderr)
                return None
            soup = BeautifulSoup(r.text, features="html.parser")
        info = self.recupInfoManga(soup)
        info["frontImage"] = self.getMangaImage(soup)
        info["urlSite"] = self.url
        info["urlInfo"] = url
        return (info)

    def __getOneChapterManga__(self, url: str, path: str)-> List[Tuple[str, int, str, str]]:
        imageList: List[Tuple[str, int, str]]

        r = getAPage(url)
        if (r == None):
            print(colored(("Problem Page for this URL: " + url, "red")))
            return (None)
        soup = BeautifulSoup(r.text, features="html.parser")
        imageList = self.getImageFromOneChapter(soup, path)
        return imageList

    def __getAllChapter__(self, url: str) -> Union[List[Tuple[str, str]], BeautifulSoup]:
        list_chapter = []

        r = getAPage(url, True)
        if (r == None):
            return None
        soup = BeautifulSoup(r.text, features="html.parser")
        list_chapter = self.recupAllChapter(soup)
        return (list_chapter, soup)

    def __removeChapterAlreadyDownloadManga__(self, chapterList:List[Tuple[str, str]], manga:Manga)->List[Tuple[str, str]] :
        path = os.path.join(manga.path, "Manga")

        if (os.path.exists(path)):
            listChapter = os.listdir(path)
            for file in listChapter :
                chapterNbr = file.replace("Chapter ", "")
                if (file != ".info.json" and os.path.isfile(os.path.join(path, file, ".info.json")) == True):
                    for i, oneChapterTuple in enumerate(chapterList):
                        if (oneChapterTuple[1] == chapterNbr):
                            chapterList.pop(i)
                            break
                elif (file != ".info.json"):
                    shutil.rmtree(os.path.join(path, file))
            return chapterList
        else:
            os.makedirs(path, exist_ok=True)
            manga.save()

    def __removeChapterAlreadyDownloadNovel__(self, chapterList:List[Tuple[str, str]], manga:Manga)->List[Tuple[str, str]] :
        path = os.path.join(manga.path, "Novel")

        if (os.path.exists(path)):
            listChapter = os.listdir(path)
            for file in listChapter :
                chapterNbr = file.replace("Chapter ", "").replace(".txt", "")
                for i, oneChapterTuple in enumerate(chapterList):
                    if (oneChapterTuple[1] == chapterNbr):
                        chapterList.pop(i)
                        break
            return chapterList
        else:
            os.makedirs(path, exist_ok=True)
            manga.save()

    def __recupAllImageFromChapterUrl__(self, urlChapterList:List[Tuple[str, str]])-> List[List[Tuple[str, int, str, str]]]:
        urlImages = []
        result = []

        with concurrent.futures.ThreadPoolExecutor() as executor :
            result = [executor.submit(self.__getOneChapterManga__, oneChapter[0], oneChapter[1]) for oneChapter in urlChapterList]

            for f in tqdm(concurrent.futures.as_completed(result), total=len(result), leave=False, desc= "    Retrieving image URLs", unit="ch"):
                urlImages.append(f.result())
        urlImages = sorted(urlImages, key = __getChapterNbr__)
        return urlImages

    def __downloadOneImage__(self, oneImage: Tuple[str, int, int, str])-> bool:
        returnValue = downloadImage(oneImage[3], oneImage[0])
        return returnValue

    def __progressBarAllInitManga__(self, urlImages: List[List[Tuple[str, int, str, str]]], mangaName: str, opts: Dict = {"workers": 5}):
        with tqdm(total=len(urlImages), desc= "    " + mangaName, unit="ch", position=0, leave=True) as bar:
            self.__downloadAllImagesThread__(urlImages, bar, opts)

    def __downloadAllImagesThread__(self, urlImages: List[List[Tuple[str, int, str, str]]], bar: tqdm = None, opts: Dict = {"workers": 5}):
        errorChapter = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=opts["workers"]) as executor :
            for urlImagesOneChapter in urlImages :
                futures_list = [executor.submit(self.__downloadOneImage__, image) for image in urlImagesOneChapter]
                for f in tqdm(concurrent.futures.as_completed(futures_list), total=len(futures_list), leave=False, desc= "        Chapter " + urlImagesOneChapter[0][2], unit="img"):
                    if (f.result() == False):
                        errorChapter.append(urlImagesOneChapter[0][2])
                        bar.write("Problem " + urlImagesOneChapter[0][2], file=sys.stderr)
                chapterInfo(len(urlImagesOneChapter), self.url, urlImagesOneChapter[0][3][:urlImagesOneChapter[0][3].rfind("\\")])
                if not (bar is None):
                    bar.update()

    def __progressBarAllInitNovel__(self, urlChapter: List[Tuple[str, str]], mangaName: str, opts: Dict):
        with tqdm(total=len(urlChapter), desc= "    " + mangaName, unit="ch", position=0, leave=True) as bar:
            self.__downloadAllNovel__(urlChapter, opts, bar)

    def __getSoupFromNovel__(self, urlOneChapter:str)->BeautifulSoup:
        r = getAPage(urlOneChapter)
        if (r == None):
            return None
        soup = BeautifulSoup(r.text, features="html.parser")
        return (soup)

    def __downoaldNovelOneChapter__(self, urlOneChapter:Tuple[str, str], opts: Dict)-> str:
        good = ""

        soup = self.__getSoupFromNovel__(urlOneChapter[0])
        if (soup != None):
            text = self.getTextFromOneChapter(soup)
            if ("trad" in opts):
                try:
                    text = translate(text, opts)
                except:
                    good = "Problem translation " + urlOneChapter[1]
            os.makedirs(os.path.dirname(urlOneChapter[1]), exist_ok=True)
            with open(urlOneChapter[1], "w+", encoding="utf-8") as file:
                file.write(text)
        else:
            good = "Problem load load URL " + urlOneChapter[1]
        return good

    def __downloadAllNovel__(self, urlChapter: List[Tuple[str, str]], opts: Dict, bar: tqdm = None):
        with concurrent.futures.ThreadPoolExecutor(max_workers=opts["workers"]) as executor :
            futures_list = [executor.submit(self.__downoaldNovelOneChapter__, urlOneChapter, opts) for urlOneChapter in urlChapter]
            for f in concurrent.futures.as_completed(futures_list):
                if (f.result() != ""):
                    bar.write("Problem " + f.result(), file=sys.stderr)
                if not (bar is None):
                    bar.update()

    def __addPathToChpterList__(self, urlChapterList:List[Tuple[str, str]], manga: Manga, mangatype: MangaType)->List[Tuple[str, str]]:
        for index, oneChapter in enumerate(urlChapterList):
            if (mangatype == MangaType.MANGA):
                urlChapterList[index] = (oneChapter[0], os.path.join(manga.path, "Manga", "Chapter " + remove(oneChapter[1].strip() ,'\\/:*?"<>|')))
            elif (mangatype == MangaType.NOVEL):
                urlChapterList[index] = (oneChapter[0], os.path.join(manga.path, "Novel", "Chapter " + remove(oneChapter[1].strip() ,'\\/:*?"<>|') + ".txt"))
        return urlChapterList

    def __createNewManga__(self, info: Dict[str, str], urlInfo: str, mangas: List[Manga], directory: str)->List[Manga]:
        correctNamePath = remove(info["name"].strip(), '\\/:*?"<>|')
        path = os.path.join(directory, correctNamePath)
        os.makedirs(path, exist_ok=True)
        pathImage = ""
        if (info["frontImage"] != ""):
            pathImage = os.path.join(path, "." + remove(info["frontImage"][info["frontImage"].rfind("/"):], '\\/:*?"<>|'))
            value = downloadImage(pathImage, info["frontImage"])
            if (value == None or False):
                pathImage = ""
        manga = Manga(info["name"], path, [(self.url, urlInfo)], [], pathImage)
        manga.save()
        mangas.append(manga)
        return (mangas)

    def __managerDownloader__(self, urlChapterList:List[Tuple[str, str]], mangas:List[Manga], urlInfo:str, opts: Dict, mangatype: MangaType, soupInfo:BeautifulSoup = None):
        manga = None
        urlImages = []

        info = self.__getInfoManga__(urlInfo, soupInfo)
        if (info == None):
            return None
        found = [x for x in mangas if x.name == info["name"]]
        if (found == []):
            mangas = self.__createNewManga__(info, urlInfo, mangas, opts["directory"])
            manga = mangas[-1]
        elif (len(found) == 1):
            if (mangatype == MangaType.MANGA):
                urlChapterList = self.__removeChapterAlreadyDownloadManga__(urlChapterList, found[0])
            elif (mangatype == MangaType.NOVEL):
                urlChapterList = self.__removeChapterAlreadyDownloadNovel__(urlChapterList, found[0])
            manga = found[0]
            if (manga.checkRegisterSite(self.url) == False):
                manga.sites = manga.sites +  [(self.url, urlInfo)]
        if (urlChapterList != None and urlChapterList != []):
            if (mangatype == MangaType.MANGA):
                self.__managerDownloaderImage__(urlChapterList, manga, opts)
            elif (mangatype == MangaType.NOVEL):
                self.__managerDownloaderText__(urlChapterList, manga, opts)
            if ("notification" in opts):
                basicNotif(opts["notification"], manga.name, len(urlChapterList), mangatype)
            manga.refresh()

    def __managerDownloaderText__(self, urlChapterList: List[Tuple[int, str]], manga: Manga, opts: Dict):
        urlChapterList = self.__addPathToChpterList__(urlChapterList, manga, MangaType.NOVEL)
        urlChapterList.reverse()
        self.__progressBarAllInitNovel__(urlChapterList, manga.name, opts)

    def __managerDownloaderImage__(self, urlChapterList: List[Tuple[int, str]], manga: Manga, opts: Dict):
        urlChapterList = self.__addPathToChpterList__(urlChapterList, manga, MangaType.MANGA)
        urlImages = self.__recupAllImageFromChapterUrl__(urlChapterList)
        self.__progressBarAllInitManga__(urlImages, manga.name, opts)

    def __getType__(self, opts: List[str] = [])->MangaType:
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
            if (len(self.siteTypeManga) == 1):
                return self.siteTypeManga[0]
            else:
                print("You need to precise what type of manga you want with the option: \"-m\" or \"-n\"")
                return MangaType.NONE
        else:
            print("This site doesn’t have any type of manga")
            return MangaType.NONE

    def __init_opt__(self, directory: str)-> Dict:
        dictio = {
            "workers": 5,
            "directory": directory
            }

        return dictio

    def __gestOpt__(self, opts: List[str], typeUrl:UrlType = UrlType.NONE, mangatype: MangaType = MangaType.NONE, directory: str = "./")-> Dict:
        dictio = self.__init_opt__(directory)

        for opt in opts :
            dictio = translateModule(dictio, opt, mangatype)
            dictio = notificationOpt(dictio, opt)
            dictio = number_worker(dictio, opt)
        return (dictio)

    def __urlManager__(self, url: str, opts: List[str], mangas: List[Manga], directory: str = "") :
        typeUrl = self.analyseURL(url)
        typemanga = self.__getType__(opts)
        urlInfo = url
        soupInfo = None
        urlChapterList = []

        if (typeUrl != UrlType.NONE and typemanga != MangaType.NONE):
            opts = self.__gestOpt__(opts, typeUrl, typemanga, directory)
            if (typeUrl == UrlType.ALLCHAPTER) :
                urlChapterList, soupInfo = self.__getAllChapter__(url)
            elif (typeUrl == UrlType.ONECHAPTER) :
                urlInfo = self.getUrlInfoFromChapter(url)
                urlChapterList = [(url, self.getChapterNbrFromUrl(url))]
            self.__managerDownloader__(urlChapterList, mangas, urlInfo, opts, typemanga, soupInfo)
