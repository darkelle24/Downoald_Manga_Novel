import os
import json

def chapterMetaData(error_list, directory):
    metadatapath = directory + ".metadata"
    if (error_list != []):
        with open(metadatapath, "w+") as meta:
            meta.write(' '.join(error_list))
    elif (os.path.isfile(metadatapath)):
        os.remove(metadatapath)

def chapterInfo(nbrImages: int, site: str, directory: str, error: bool = False):
    infoPath = os.path.join(directory, ".info.json")
    os.makedirs(os.path.dirname(infoPath), exist_ok=True)
    info = {"site": site, "nbrImages": str(nbrImages), "error": error}
    with open(infoPath, "w+") as infoFile:
            json.dump(info, infoFile, indent=4)
