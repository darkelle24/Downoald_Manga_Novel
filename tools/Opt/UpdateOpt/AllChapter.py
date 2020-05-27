from typing import Dict

def allOpt(dictio: Dict, opt: str)-> Dict:
    if (opt == "-a" or opt == "--allChapter"):
        dictio["allChapter"] = True
    return dictio