# No Man's Sky Portal Address Reader

**English** | [日本語](README.ja.md)

Recognize portal glyphs from the screenshot with OpenCV and Python.

- Currently unstable
- Support resolutions:
    - 1920x1080, 1920x1200, 1920x1440, 2048x1536, 2560x1440, 2560x1600, 3840x2160, (1280x720)
- Output the following:
    - Array of portal number
    - 12-digit hex (for Portal Glyph Font)
    - Comparison images for visual verification of results

## Usage

- Copy `config.sample.ini` as `config.ini`
- Install `OpenCV` , `Python` and `pipenv` on your OS
    - For Debian/Ubuntu, use `libopencv-dev` package for OpenCV
- Install the dependencies with `pipenv install`
- Store screenshots with the portal address in the `screenshots` directory
    - By default, the target files are `screenshots/*.jpg`
- Run `pipenv run main`
    - If you want to save the output to a file, use `pipenv run main > result.txt`
- The visual confirmation image is output to `result.jpg`
