#!/usr/bin/python3

"""
Gets a directory and scans for images
Produces a report in CSV of metadata for each image
"""

import sys
import os
import logging
import imghdr
from PIL import Image
import csv

logging.basicConfig(filename='debug.log',level=logging.DEBUG)


def find_images(path):
    formats = ["jpeg", "jpg", "png"]
    imageList = []
    for root, dirs, files in os.walk(path):
        logging.debug("WTF")
        logging.debug([root, dirs, files])
        imageList += [os.path.join(root, candidate) for candidate in files if imghdr.what(os.path.join(root, candidate)) in formats]
        logging.debug("Images found at {root}: {images}".format(root=root, images=imageList))
        for d in dirs:
            imageList += find_images(os.path.join(root, d))
    return imageList

def calc_meta(imagePath):
    im = Image.open(imagePath)
    meta = {}
    meta["format"] = im.format
    meta["mode"] = im.mode
    meta["width"], meta["height"] = im.size
    meta["pixels"] = im.width * im.height
    meta["path"] = imagePath
    try:
        for tag in exifPairs:
            meta[ExifTags.TAGS[tag]] = im.getexif()[tag]
    except:
        logging.warning("Could not get EXIF data from {image}".format(image=imagePath))
    im.close()
    logging.debug("Meta for {path} calculated {meta}".format(path=imagePath, meta=meta))
    return meta


def save_image_meta(metaList, outPath):
    logging.debug(metaList)
    with open(outPath, 'w') as f:
        dict_writer = csv.DictWriter(f, metaList[0].keys(), delimiter=',', quotechar='\"', quoting=csv.QUOTE_ALL)
        dict_writer.writeheader()
        dict_writer.writerows(metaList)


if __name__ == "__main__":
    logging.info("Image Dump Run Starting...")
    path = sys.argv[1]
    out = sys.argv[2]
    if not os.path.exists(path):
        print(path, "does not exist")
        sys.exit()
    if os.path.exists(out):
        print("Output location", out, "exists. Aborting...")
        sys.exit()
    images = find_images(path)
    logging.info(images)
    logging.info("Total images found: {count}".format(count=len(images)))
    image_meta = [calc_meta(image) for image in images]
    save_image_meta(image_meta, out)
    print("Output stored at", out)

