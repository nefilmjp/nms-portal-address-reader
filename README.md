# No Man's Sky Portal Address Reader

**English** | [日本語](README.ja.md)

Read portal address from screenshot with OpenCV and Python.

- Currently unstable
- Supports a resolution of 1920x1080
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
