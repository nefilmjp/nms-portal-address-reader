import configparser
import math
import cv2
import numpy as np
from typing import Union
from utils.resolutions import resolutions

ini = configparser.ConfigParser()
ini.read("./config.ini", "UTF-8")
config = ini["DEFAULT"]

def read_screenshot(path):
    img = cv2.imread(path, cv2.IMREAD_COLOR)
    h, w, _ = img.shape
    if w > 1920:
        return cv2.resize(img, (1920, round(1920 / w * h)))
    return img

def crop_address(img: cv2.Mat, profile: dict[str, Union[int, float]]):
    # print(profile)
    top = profile["y"]
    bottom = top + profile["box"]
    left = profile["x"]
    right = left + profile["box"] * 12

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


def get_glyph_from_address(img: cv2.Mat, pos: int, resolution: dict[str, Union[int, float]]):
    """pos: 0-11"""
    top = 0
    bottom = resolution["box"]
    left = resolution["box"] * pos + round(resolution["offset"] * pos)
    right = left + resolution["box"]
    # cv2.imwrite(f".temp/{pos}.png", img[top:bottom, left:right])
    return img[top:bottom, left:right]


def get_glyph_from_standard(img: cv2.Mat, pos: int):
    """pos: 0-15"""
    top = 0
    bottom = 32
    left = 32 * pos
    right = left + 32
    return img[top:bottom, left:right]


def parse_standard(path: str):
    akaze = cv2.AKAZE_create()

    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

    std_descs = []
    std_kps = []
    std_samples = []
    std_thumbs = []

    for pos in range(16):
        glyph = get_glyph_from_standard(img, pos)

        sample = cv2.resize(
            glyph, (320, 320), None, None, None, cv2.INTER_NEAREST
        )

        kp, des = akaze.detectAndCompute(sample, None)

        std_kps.append(kp)
        std_descs.append(des)
        std_samples.append(sample)
        std_thumbs.append(glyph)

    return [std_kps, std_descs, std_samples, std_thumbs]


def get_resolution(img: cv2.Mat):
    h, w, _ = img.shape
    if (resolutions[w] is None):
        return False
    if (resolutions[w][h] is None):
        return False
    return resolutions[w][h]


def match_address(img: cv2.Mat, std_kps, std_descs, resolution):
    akaze = cv2.AKAZE_create()
    bf = cv2.BFMatcher()

    result = []
    address = crop_address(img, resolution)

    for pos in range(12):
        glyph = get_glyph_from_address(address, pos, resolution)

        sample = cv2.resize(
            glyph, (320, 320), None, None, None, cv2.INTER_NEAREST
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

            # print(f"letter{pos + 1} glyph{idx + 1} {len(good_matches)}/{len(matches)}")

            if(len(matches) > 0):
                good_ratio.append(len(good_matches) / len(matches))
            else:
                good_ratio.append(0)

        max_value = max(good_ratio)
        max_index = good_ratio.index(max_value)
        result.append(max_index + 1)

    return result
