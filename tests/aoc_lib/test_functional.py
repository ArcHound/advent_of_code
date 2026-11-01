import datetime

# vim: nomodeline
import json
from unittest.mock import patch, mock_open
import pytest

from aoc_lib.functional import *

from aoc_lib.map2d import Map2d


def test_binom():
    example_map = """........
........
..####..
..#....."""

    map2d = Map2d.from_lines(example_map)
    print(map2d.debug_draw())
    map_start = (1, 1)
    map_end = (3, 3)

    def map_is_done(point):
        return point == map_end

    def map_legal_moves(point):
        result = list()
        points = map2d.nearby_points(point)
        for p in points:
            if map2d.get_point(p) == ".":
                result.append((p, 1))
        return result

    cases = [
        {
            "label": "flood",
            "input": {
                "start": map_start,
                "is_done": map_is_done,
                "legal_moves": map_legal_moves,
            },
            "output": 10,
            "ex": None,
        },
    ]
    for case in cases:
        try:
            output = bfs(**case["input"])
            assert output == case["output"], "case '{}', output: exp {}, got {}".format(
                case["label"], case["output"], output
            )
        except Exception as e:
            assert type(e) == case["ex"], "case '{}', ex: exp {}, got {}".format(
                case["label"], case["ex"], type(e)
            )
