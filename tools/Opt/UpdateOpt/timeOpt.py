import time
from typing import Dict


def timerOpt(dictio: Dict, opt: str)-> Dict:
    if (opt.startswith("--timed=")):
        timer = int(opt[8:])
        dictio["timer"] = timer
    return dictio
