from genericpath import isdir
import img2pdf
import os
from PIL import Image
from io import BytesIO
from distutils.dir_util import copy_tree
from multiprocessing import Pool
from math import *

def getNameDir(dir):
    try:
        return float(dir.split()[1])
    except ValueError:
        return -2

def getAllPdf(path):
    start = "./Manga"

    dirs = os.listdir(start)
    dirs.sort(key=getNameDir)
    
    with Pool(processes= 5) as pool:
        for dirname in dirs:
            pathGet = os.path.join(start, dirname)
            if (os.path.isdir(pathGet)):
                pathSave = os.path.join(path, dirname + '.pdf')
                pool.apply_async(getOnePdf, args=(pathSave, pathGet, os.path.join(path, dirname)))
        pool.close()
        pool.join()

def getName(file):
    if (file == '.info.json'):
        return -1
    else:
        nbr = file.split('.')[0]
        try:
            return int(nbr)
        except ValueError:
            return -2

def openFile(image):
    return Image.open(image)

def get_concat_v(im1, im2):
    dst = Image.new('RGB', (im1.width, im1.height + im2.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (0, im1.height))
    return dst

def reduceFile(images):
    openMap = list(map(openFile, images))
    widthA4 = 595
    heightA4 = 842
    toReturn = []
    newImage = None

    for oneImage in openMap:
        width, height = oneImage.size
        try:
            resizeImage = oneImage.resize((widthA4, ceil((height/width) * widthA4)))
            if (newImage == None):
                newImage = resizeImage
            else:
                newImage = get_concat_v(newImage, resizeImage)
        except e:
            print(e)
    newWidth, newHeight = newImage.size
    numberPart = ceil(newHeight / heightA4)
    for x in range(numberPart):
        cropImage = newImage.crop((0, x * heightA4, widthA4, (x+1) * heightA4))
        output = BytesIO()
        cropImage.save(output, format='JPEG', optimize=True, quality=65)
        toReturn.append(output.getvalue())

    for oneImage in openMap:
        oneImage.close()
    return toReturn


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

    images = reduceFile(images)

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