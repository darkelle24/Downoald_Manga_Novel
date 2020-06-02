from typing import Dict

def number_worker(dictio: Dict, opt: str)-> Dict:
    if (opt.startswith("--workers=") == True):
        dictio["workers"] = int(opt[10:])
    return dictio