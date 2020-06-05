from typing import Dict
import sys
from tools.Other.checkModuleExist import module_exists
from include.Enum import MangaType

def notificationOpt(dictio: Dict, opt: str)-> Dict:
    if (opt == ("-N") or opt == ("--notification")):
        if "notification" not in sys.modules:
            if (module_exists("plyer") == True):
                notif = __import__("plyer")
                dictio["notification"] = notif
            else:
                print("To use Traduction module you need to install plyer: pip install -I https://github.com/kivy/plyer/zipball/master")
        else:
            dictio["notification"] = sys.modules["notification"]
    return dictio

def basicNotif(notifModule, name: str, nbrChapter: int, mangaType: MangaType):
    if (mangaType == MangaType.MANGA):
        mangatype = "MANGA"
    else:
        mangatype = "NOVEL"
    notifModule.notification.notify(
        title='Finish Download ' + mangatype,
        message=name + "\n\nDownload " + str(nbrChapter) + " chapters",
        app_name='Manga Downloader',
        app_icon=r'.\Resource\icon.ico',
        ticker='Finish Download ' + mangatype
    )