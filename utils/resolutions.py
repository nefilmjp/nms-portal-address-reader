from typing import Union

resolutions: dict[int, dict[int, dict[str, Union[int, float]]]] = {
    1280: {
        720: {
            "x": 8,
            "y": 676,
            "box": 22,
            "offset": -0.7,
        },
    },
    1920: {
        1080: {
            "x": 11,
            "y": 1015,
            "box": 32,
            "offset": 0,
        },
        1200: {
            "x": 11,
            "y": 1127,
            "box": 32,
            "offset": 0,
        },
        1440: {
            "x": 11,
            "y": 1352,
            "box": 32,
            "offset": 0,
        },
    },
}
