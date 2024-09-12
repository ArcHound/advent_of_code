# 2019-8
import logging
import functools
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

log = logging.getLogger("aoc_logger")
width_c = 25
height_c = 6


def parse_data(in_data, width=width_c, height=height_c):
    wc = 0
    hc = 0
    layers = list()
    buffer = list()
    layer = list()
    for i in range(len(in_data.strip())):
        if i % width == 0 and i != 0 and i % (width * height) != 0:
            # log.info(f"Appending buffer at {i}")
            layer.append(buffer)
            # log.info(layer)
            buffer = list()
            buffer.append(in_data[i])
        elif i % width == 0 and i != 0 and i % (width * height) == 0:
            # log.info(f"Appending layer at {i}")
            layer.append(buffer)
            layers.append(layer)
            layer = list()
            buffer = list()
            buffer.append(in_data[i])
        elif i % width != 0 or i == 0:
            buffer.append(in_data[i])
    return layers


def part1(in_data, test=False):
    data = parse_data(in_data)
    scores = list()
    for layer in data:
        score = {"0": 0, "1": 0, "2": 0}
        for row in layer:
            for c in row:
                score[c] += 1
        scores.append(score)
    scores_sorted = sorted(scores, key=lambda x: x["0"])
    return scores_sorted[0]["1"] * scores_sorted[0]["2"]


def part2(in_data, test=False):
    data = parse_data(in_data)
    image = list()
    for j in range(height_c):
        row = list()
        for i in range(width_c):
            done = False
            for layer in data:
                if layer[j][i] == "2":
                    continue
                else:
                    row.append(layer[j][i])
                    done = True
                if done:
                    break
            if not done:
                row.append("2")
        image.append(row)

    for row in image:
        for i in range(len(row)):
            if row[i] == "0":
                row[i] = (0, 0, 0)
            elif row[i] == "1":
                row[i] = (255, 255, 255)
            elif row[i] == "2":
                row[i] = (255, 0, 0)
    for row in image:
        log.info(len(row))
    array = np.array(image, dtype=np.uint8)
    new_image = Image.fromarray(array)
    new_image.save("day8_part2.png")
    return 0
