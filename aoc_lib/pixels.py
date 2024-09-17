from PIL import Image
import numpy as np

import logging

log = logging.getLogger("aoc_logger")

default_pixel_map = {
    0: [0, 0, 0],
    1: [255, 255, 255],
    2: [255, 0, 0],
    3: [0, 255, 0],
    4: [0, 0, 255],
    5: [255, 255, 0],
    6: [0, 255, 255],
    7: [255, 0, 255],
}


def map_pixel_dict(pixel_dict, pixel_map=default_pixel_map):
    new_dict = dict()
    for k in pixel_dict:
        new_dict[k] = pixel_map[pixel_dict[k]]
    return new_dict


def dict_to_array(pixel_dict, default_color=[0, 0, 0]):
    # find bounds
    xs = [k[0] for k in pixel_dict.keys()]
    ys = [k[1] for k in pixel_dict.keys()]
    bounds = ((min(xs), min(ys)), (max(xs), max(ys)))
    # log.debug(bounds)
    x_len = bounds[1][0] - bounds[0][0] + 1
    y_len = bounds[1][1] - bounds[0][1] + 1
    # image data
    data = np.zeros((x_len, y_len, 3), dtype=np.uint8)
    for i in range(x_len):
        for j in range(y_len):
            if (bounds[0][0] + i, bounds[0][1] + j) in pixel_dict:
                data[i, j] = pixel_dict[bounds[0][0] + i, bounds[0][1] + j]
            else:
                data[i, j] = default_color
    return data


def draw_array(data):
    image = Image.fromarray(data)
    # log.debug(image.size)
    image.show()


def default_draw(pixel_dict):
    p_dict = map_pixel_dict(pixel_dict)
    arr = dict_to_array(p_dict)
    draw_array(arr)
