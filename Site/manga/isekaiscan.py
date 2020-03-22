from tools.getPage import *
from Site.ISite import *
from tools.downloadImage import *
from tools.progress_bar import *
from tools.SiteMetaData import *

class isekaiscan:
    @staticmethod
    def getOneChapter(url, directory):
        nbr_image = 0
        error_list = []
        r = get_an_page(url)
        if (r == None):
            print(colored(("Problem Page for Chapter" + directory.split(" ")[-1].replace("\\", ""), "red")))
            return (error_list)
        soup = BeautifulSoup(r.text, features="html.parser")
        for link in soup.find_all('img'):
            if (link.has_attr("id") == True and link.get("id").find("image") != -1):
                nbr_image += 1
                url = link.get("data-src").lstrip()
                nbr = link.get("id").replace("image-", "")
                path = directory + nbr + "." + url.split(".")[-1]
                if (downloadImage(path, url) == False):
                    error_list.append(int(nbr))
        chapterMetaData(error_list, directory)
        return error_list
                    
                
    @staticmethod
    def InfoOneChapter(one_chapter):
        return one_chapter.get("href"), one_chapter.string.strip().split(" ")[-1]

    @staticmethod
    def getAllChapter(url, directory):
        list_chapter = []
        r = get_an_page(url)
        if (r == None):
            return None
        soup = BeautifulSoup(r.text, features="html.parser")
        ul = soup.find("ul", attrs={"class": "main version-chap"})
        if (ul == None):
            return None
        for one_chapter in ul.find_all("li"):
            if (one_chapter.has_attr("class") == True and one_chapter.get("class")[0].find("wp-manga-chapter") != -1):
                list_chapter.append(one_chapter.a)
        progress_bar_all_chapter(list_chapter, isekaiscan, directory)

    @staticmethod
    def urlDownload(url, directory):
        parse_url = url.split("/")
        if (len(parse_url) <= 4 or (len(parse_url) == 5 and parse_url[4] == "")):
            print ("Wrong URL for isekaiscan site web")
            return None
        else:
            directory = directory + "manga\\" + parse_url[4] + "\\"
            if (len(parse_url) == 6 and parse_url[5].find("chapter-") != -1):
                directory = directory + "Chapter " + parse_url[5].replace("chapter-", "").replace("-", ".") + "\\"
                isekaiscan.getOneChapter(url, directory)
            else:
                isekaiscan.getAllChapter(url, directory)