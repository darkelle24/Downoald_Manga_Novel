import os
from typing import Dict, List, Tuple, Union
import time

from bs4 import BeautifulSoup

from include.Site import MangaType, Site, UrlType
from tools.Other.getPage import getAPage


class mangarock(Site):
    url = "mangarockteam.com"
    siteTypeManga = [MangaType.MANGA]

    def recupInfoManga(self, soup: BeautifulSoup)-> Dict[str, str]:
        info = dict()
        name = soup.find("h1")
        if (name.string == None):
            name = name.text.replace("HOT", "").replace("NEW", "").strip()
        else:
            name = name.string.replace("HOT", "").replace("NEW", "").strip()
        info["name"] = name
        return info

    def getImageFromOneChapter(self, soup: BeautifulSoup, path: str)->List[Tuple[str, int, int, str]]:
        images = []

        splitted = path.split('\\')
        good = False
        i = 1
        chapter = splitted[-1].split()[i * -1]
        while (good != True):
            try:
                float(chapter)
                good = True
            except ValueError:
                i = i + 1
                chapter = splitted[-1].split()[i * -1]
        for link in soup.find_all('img'):
            if (link.has_attr("id") == True and link.get("id").find("image") != -1):
                url = link.get("data-src").lstrip()
                nbr = link.get("id").replace("image-", "")
                images.append((url, int(nbr), chapter, os.path.join(path, nbr + url[url.rfind("."):])))
        return (images)

    def recupAllChapter(self, soup: BeautifulSoup) -> List[Tuple[str, str]]:
        list_chapter = []

        time.sleep(1)
        ul = soup.find("ul", attrs={"class": "main"})
        if (ul == None):
            return None
        for one_chapter in ul.find_all("li"):
            if (one_chapter.has_attr("class") == True and one_chapter.get("class")[0].find("wp-manga-chapter") != -1):
                list_chapter.append((one_chapter.a.get("href"), one_chapter.a.string.strip().replace("Chapter", "").replace("chapter", "").strip()))
        return (list_chapter)

    def getChapterNbrFromUrl(self, urlChapter: str)-> str:
        if (urlChapter[-1] == "/"):
            urlChapter = urlChapter[:-1]
        return urlChapter[urlChapter.rfind("/"):].replace("chapter-", "").replace("/", "").strip()

    def analyseURL(self, url:str)->UrlType :
        if (url[-1] == "/"):
            url = url[:-1]
        parse_url = url.split("/")
        if (len(parse_url) == 6 and parse_url[5].find("chapter-") != -1):
            return UrlType.ONECHAPTER
        else:
            return UrlType.ALLCHAPTER

    def getMangaImage(self, soup: BeautifulSoup)-> str :
        img = soup.find("div", attrs={"class": "summary_image"}).find("img")
        return img.get("data-src")
