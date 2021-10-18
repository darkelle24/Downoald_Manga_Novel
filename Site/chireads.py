import os
from typing import Dict, List, Tuple, Union

from bs4 import BeautifulSoup

from include.Site import MangaType, Site, UrlType
from tools.Other.getPage import getAPage


class chireads(Site):
    url = "chireads.com"
    siteTypeManga = [MangaType.NOVEL]

    def recupInfoManga(self, soup: BeautifulSoup)-> Dict[str, str]:
        info = dict()

        name = soup.find("h3", attrs={"class": "inform-title"})
        if (name.string == None):
            name = name.text.replace("HOT", "").replace("NEW", "").strip()
        else:
            name = name.string.replace("HOT", "").replace("NEW", "").strip()
        info["name"] = name
        return info

    def getTextFromOneChapter(self, soupOneChapter: BeautifulSoup)->str:
        text = ""

        ##chapter = soupOneChapter.find("div", attrs={"class": "text-left"})
        temp = soupOneChapter.find("div", attrs={"id": "content"})
        if (temp != None):
            chapter = temp
        for textget in chapter.find_all('p'):
            if (textget.string != None):
                if (textget.string != "\n"):
                    text = text + textget.string + "\n\n"
                else:
                    text = text + textget.string
        return (text.replace("\n\n\n", "\n\n"))

    def recupAllChapter(self, soup: BeautifulSoup) -> List[Tuple[str, str]]:
        list_chapter = []

        ul = soup.find('div', attrs={"class": "chapitre-table"}).find("ul")
        if (ul == None):
            return None
        for one_chapter_li in ul.find_all("li"):
            for one_chapter in one_chapter_li.find_all("a"):
                list_chapter.append((one_chapter.get("href"), one_chapter.string.replace("Chapitre ", "").replace("&nbsp;", "").strip()))
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
        img = soup.find("div", attrs={"class": "inform-product"}).find("img")
        return img.get("src")
