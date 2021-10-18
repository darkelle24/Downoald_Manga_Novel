from genericpath import isdir
import img2pdf
import os
from PIL import Image
from distutils.dir_util import copy_tree

def getNameDir(dir):
    try:
        return float(dir.split()[1])
    except ValueError:
        return -2

def getAllPdf(path):
    start = "./Manga"

    dirs = os.listdir(start)
    dirs.sort(key=getNameDir)
    for dirname in dirs:
        pathGet = os.path.join(start, dirname)
        if (os.path.isdir(pathGet)):
            pathSave = os.path.join(path, dirname + '.pdf')
            getOnePdf(pathSave, pathGet, os.path.join(path, dirname))

def getName(file):
    if (file == '.info.json'):
        return -1
    else:
        nbr = file.split('.')[0]
        try:
            return int(nbr)
        except ValueError:
            return -2

def getOnePdf(pathSave, pathGet, pathError):
    files = os.listdir(pathGet)
    if (len(files) <= 1):
        return
    files.sort(key=getName)

    images = []
    for file in files:
        if (file != '.info.json'):
            filepath = os.path.join(pathGet, file)
            images.append(filepath)

    error = False
    with open(pathSave,"wb") as f:
        try:
	        f.write(img2pdf.convert(images))
        except:
            error = True
    if (error == True):
        copy_tree(pathGet, pathError)
    if error == True and os.path.exists(pathSave):
        os.remove(pathSave)

def main():
    directory = './PDF'
    if (not(os.path.isdir(directory))):
        os.mkdir(directory)
    
    getAllPdf(directory)

if (__name__== "__main__"):
    main()