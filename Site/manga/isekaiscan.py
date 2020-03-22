from tools.getPage import *
from Site.ISite import *
from tools.downloadImage import *

class isekaiscan:
    @staticmethod
    def getOneChapter(url, directory):
        r = get_an_page(url)
        if (r == None):
            return None
        soup = BeautifulSoup(r.text, features="html.parser")
        for link in soup.find_all('img'):
            if (link.has_attr("id") == True and link.get("id").find("image") != -1):
                url = link.get("data-src").lstrip()
                path = directory + "Chapter_" + url.split("/", 4)[-1][8:]
                downloadImage(path, url)
                

    @staticmethod
    def getAllChapter(url, directory):
        r = get_an_page(url)
        if (r == None):
            return None
        soup = BeautifulSoup(r.text, features="html.parser")
        ul = soup.find("ul", attrs={"class": "main version-chap"})
        if (ul == None):
            return None
        for one_chapter in ul.find_all("li"):
            if (one_chapter.has_attr("class") == True and one_chapter.get("class")[0].find("wp-manga-chapter") != -1):
                isekaiscan.getOneChapter(one_chapter.a.get("href"), directory)

    @staticmethod
    def urlDownload(url, directory):
        parse_url = url.split("/")
        if (len(parse_url) <= 4 or (len(parse_url) == 5 and parse_url[4] == "")):
            print ("Wrong URL for isekaiscan site web")
            return None
        else:
            directory = directory + "manga\\" + parse_url[4] + "\\"
            if (url.find("chapter-") != -1):
                isekaiscan.getOneChapter(url, directory)
            else:
                isekaiscan.getAllChapter(url, directory)