import os

def chapterMetaData(error_list, directory):
    metadatapath = directory + ".metadata"
    if (error_list != []):
        with open(metadatapath, "w+") as meta:
            meta.write(' '.join(error_list))
    elif (os.path.isfile(metadatapath)):
        os.remove(metadatapath)