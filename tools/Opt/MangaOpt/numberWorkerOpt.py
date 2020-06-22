from typing import Dict

def number_worker(dictio: Dict, opt: str)-> Dict:
    if (opt.startswith("--workers=") == True):
        if (len(opt) > 10):
            dictio["workers"] = int(opt[10:])
        else:
            dictio["workers"] = 5
    return dictio