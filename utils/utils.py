import configparser
import math
import cv2
import numpy as np

ini = configparser.ConfigParser()
ini.read("./config.ini", "UTF-8")
config = ini["DEFAULT"]


def read_screenshot(path):
    img = cv2.imread(path, cv2.IMREAD_COLOR)
    return img


def crop_address(img: cv2.Mat):
    top = config.getint("addrPosY")
    bottom = top + config.getint("glyphHeight")
    left = config.getint("addrPosX")
    right = left + config.getint("glyphWidth") * 12

    img_cropped = img[top:bottom, left:right]
    img_invert = np.invert(img_cropped)
    img_gray = cv2.cvtColor(img_invert, cv2.COLOR_BGR2GRAY)

    hsv = cv2.cvtColor(img_invert, cv2.COLOR_BGR2HSV)
    _, _, v = cv2.split(hsv)

    if np.std(v) < config.getint("claheValueThreshold"):
        clahe = cv2.createCLAHE(
            clipLimit=config.getfloat("claheClipLimit"),
            tileGridSize=(
                config.getint("claheTileGridSizeX"),
                config.getint("claheTileGridSizeY"),
            ),
        )
        return clahe.apply(img_gray)

    return img_gray


def get_glyph_from_address(img: cv2.Mat, pos: int):
    """pos: 0-11"""
    top = 0
    bottom = config.getint("glyphHeight")
    left = config.getint("glyphWidth") * pos
    right = left + config.getint("glyphWidth")
    return img[top:bottom, left:right]


def get_glyph_from_standard(img: cv2.Mat, pos: int):
    """pos: 0-15"""
    top = 0
    bottom = config.getint("glyphHeight")
    left = config.getint("glyphWidth") * pos
    right = left + config.getint("glyphWidth")
    return img[top:bottom, left:right]


def parse_standard():
    akaze = cv2.AKAZE_create()

    img = cv2.imread(config.get("standard"), cv2.IMREAD_GRAYSCALE)

    sample_width = config.getint("glyphWidth") * config.getint("glyphMultiplier")
    sample_height = config.getint("glyphHeight") * config.getint("glyphMultiplier")

    std_descs = []
    std_kps = []
    std_samples = []
    std_thumbs = []

    for pos in range(16):
        glyph = get_glyph_from_standard(img, pos)

        sample = cv2.resize(
            glyph, (sample_width, sample_height), None, None, None, cv2.INTER_NEAREST
        )

        kp, des = akaze.detectAndCompute(sample, None)

        std_kps.append(kp)
        std_descs.append(des)
        std_samples.append(sample)
        std_thumbs.append(glyph)

    return [std_kps, std_descs, std_samples, std_thumbs]


def match_address(img: cv2.Mat, std_kps, std_descs):
    akaze = cv2.AKAZE_create()
    bf = cv2.BFMatcher()

    sample_width = config.getint("glyphWidth") * config.getint("glyphMultiplier")
    sample_height = config.getint("glyphHeight") * config.getint("glyphMultiplier")

    result = []
    address = crop_address(img)

    for pos in range(12):
        glyph = get_glyph_from_address(address, pos)

        sample = cv2.resize(
            glyph, (sample_width, sample_height), None, None, None, cv2.INTER_NEAREST
        )

        kp, des = akaze.detectAndCompute(sample, None)

        good_ratio = []

        for idx, query_des in enumerate(std_descs):
            query_kp = std_kps[idx]
            matches = bf.knnMatch(des, query_des, k=2)

            good_matches = []

            for query, train in matches:
                x1, y1 = query_kp[query.trainIdx].pt
                x2, y2 = kp[train.queryIdx].pt
                length = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                if (
                    query.distance < train.distance * config.getfloat("bfmDistance")
                ) and length < config.getint("bfmLengthLimit"):
                    good_matches.append(query)

            good_ratio.append(len(good_matches) / len(matches))

        max_value = max(good_ratio)
        max_index = good_ratio.index(max_value)
        result.append(max_index + 1)

    return result
