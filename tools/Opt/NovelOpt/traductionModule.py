from tools.Other.checkModuleExist import module_exists
from include.Enum import MangaType
from typing import List, Dict
import sys

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
                        dictio["trad"] = (trad.Translator(), lang)
                    else:
                        print("The language "+ lang + " is not available")
                else:
                    print("To use Traduction module you need to install googletrans: pip install googletrans")
            else:
                dictio["trad"] = (sys.modules["googletrans"].Translator(), lang)
        else:
            print("Traduction module is only available for Novel type")
    return dictio