import configparser
import os
import glob
import cv2
from utils import utils

ini = configparser.ConfigParser()
ini.read("./config.ini", "UTF-8")
config = ini["DEFAULT"]


def main():
    screenshots = glob.glob(config.get("screenshotsGlob"))
    screenshots.sort()

    std_kps, std_descs, _, std_thumbs = utils.parse_standard()

    thumb_parts = []

    for path in screenshots:
        ss = utils.read_screenshot(path)
        basename = os.path.basename(path)
        #filename = os.path.splitext(basename)[0]

        result = utils.match_address(ss, std_kps, std_descs)

        thumbs = []
        hex_string = ""

        for glyph_num in result:
            hex_string = hex_string + str(hex(glyph_num - 1))[2:].upper()
            thumbs.append(std_thumbs[glyph_num - 1])

        thumb_ss = utils.crop_address(ss)
        thumb_glyph = cv2.hconcat(thumbs)
        thumb_parts.append(thumb_ss)
        thumb_parts.append(thumb_glyph)
        thumb_parts.append(cv2.subtract(thumb_ss, thumb_glyph))

        print(basename, hex_string, result)

    cv2.imwrite(config.get("resultImage"), cv2.vconcat(thumb_parts))


if __name__ == "__main__":
    main()
