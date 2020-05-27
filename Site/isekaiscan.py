from include.Site import Site, UrlType, MangaType
from typing import Tuple, List, Union, Dict
from bs4 import BeautifulSoup
from tools.Other.getPage import getAPage
import os

class isekaiscan(Site):
    url = "isekaiscan.com"
    siteTypeManga = [MangaType.MANGA]

    def recupInfoManga(self, soup: BeautifulSoup, info: Dict[str, str])-> Dict[str, str]:
        name = soup.find("h3")
        if (name.string == None):
            name = name.text.replace("HOT", "").replace("NEW", "").strip()
        else:
            name = name.string.replace("HOT", "").replace("NEW", "").strip()
        info["name"] = name
        return info

    def recupOneChapter(self, soup: BeautifulSoup, path: str)->List[Tuple[str, int, str, str]]:
        images = []

        chapter = soup.find("h1", attrs={"id": "chapter-heading"})
        chapter = chapter.string.split(" ")[-1]
        for link in soup.find_all('img'):
            if (link.has_attr("id") == True and link.get("id").find("image") != -1):
                url = link.get("data-src").lstrip()
                nbr = link.get("id").replace("image-", "")
                images.append((url, int(nbr), chapter, os.path.join(path, nbr + url[url.rfind("."):])))
        return (images)

    def recupAllChapter(self, soup: BeautifulSoup) -> List[Tuple[str, str]]:
        list_chapter = []

        ul = soup.find("ul", attrs={"class": "main version-chap"})
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