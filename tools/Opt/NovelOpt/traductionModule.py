import sys
import time
from math import *
from typing import Dict, List

from include.Enum import MangaType
from tools.Other.checkModuleExist import module_exists


def translateModule(dictio: Dict, opt: str, mangatype: MangaType)-> Dict:
    if (opt.startswith("-t") or opt.startswith("--trad=")):
        if (mangatype == MangaType.NOVEL):
            if "googletrans" not in sys.modules:
                if (module_exists("googletrans") == True):
                    if (opt.startswith("-t")):
                        lang = "fr"
                    else:
                        lang = opt.replace("--trad=", "")
                    trad = __import__("googletrans")
                    if (lang in trad.LANGUAGES):
                        dictio["trad"] = (trad, lang)
                    else:
                        print("The language "+ lang + " is not available")
                else:
                    print("To use Traduction module you need to install googletrans: pip install googletrans")
            else:
                if (opt.startswith("-t")):
                    lang = "fr"
                else:
                    lang = opt.replace("--trad=", "")
                dictio["trad"] = (sys.modules["googletrans"], lang)
        else:
            print("Traduction module is only available for Novel type")
    return dictio

def translate(texts: str, opts: Dict)-> str:
    finale = ""
    list_txt = []
    pos = 0
    copy = texts
    dest = opts["trad"][1]
    translator = opts["trad"][0].Translator()

    ##text = opts["trad"][0].translate(text, dest=opts["trad"][1], src="en").text
    while (pos != -1 and len(copy) > 5000):
        pos = copy.rfind("\n", 0, 5000)
        list_txt = list_txt + [copy[:pos]]
        copy = copy[pos:]
    list_txt = list_txt + [copy]
    for txt in list_txt:
        finale = finale + translator.translate(txt, dest=dest, src="en").text
        time.sleep(1)
    return finale
