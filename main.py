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

    profile = config.get("profile")
    std_kps, std_descs, _, std_thumbs = utils.parse_standard(f"profiles/{profile}.png")

    thumb_parts = []

    for path in screenshots:
        ss = utils.read_screenshot(path)
        basename = os.path.basename(path)
        #filename = os.path.splitext(basename)[0]

        resolution = utils.get_resolution(ss)

        result = utils.match_address(ss, std_kps, std_descs, resolution)

        thumbs = []
        hex_string = ""

        for glyph_num in result:
            hex_string = hex_string + str(hex(glyph_num - 1))[2:].upper()
            thumbs.append(std_thumbs[glyph_num - 1])

        # thumb_ss = utils.crop_address(ss)
        # thumb_ss = cv2.resize(utils.crop_address(ss, resolution), (32 * 12, 32))
        thumb_ss = cv2.resize(utils.get_thumb_ss(ss, resolution), (32 * 12, 32))
        thumb_glyph = cv2.hconcat(thumbs)
        thumb_parts.append(thumb_ss)
        thumb_parts.append(thumb_glyph)
        # thumb_parts.append(cv2.subtract(thumb_ss, thumb_glyph))

        print(basename, hex_string, result)

    mergedResult = cv2.vconcat(thumb_parts)
    cv2.imwrite(config.get("resultImage"), mergedResult)


if __name__ == "__main__":
    main()
