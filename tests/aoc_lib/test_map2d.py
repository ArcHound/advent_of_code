import datetime

# vim: nomodeline
import json
from unittest.mock import patch, mock_open
import pytest

from aoc_lib.map2d import Map2d, PipeType, PipeMap2d


def test_init_ex():
    cases = [
        {
            "label": "simple",
            "init": {
                "obstacle_str": "..........#......#......#........................",
                "bounds": ((0, 0), (7, 7)),
            },
            "ex": None,
        },
        {
            "label": "rectangle",
            "init": {
                "obstacle_str": ".........#......#......#............",
                "bounds": ((0, 0), (9, 4)),
            },
            "ex": None,
        },
        {
            "label": "smol bounds",
            "init": {
                "obstacle_str": ".........#......#......#.....................",
                "bounds": ((0, 0), (4, 4)),
            },
            "ex": ValueError,
        },
        {
            "label": "Big bounds",
            "init": {
                "obstacle_str": ".........#......#......#.....................",
                "bounds": ((0, 0), (14, 14)),
            },
            "ex": ValueError,
        },
    ]
    for case in cases:
        try:
            obj = Map2d(**case["init"])
            # assert output == case["output"], "case '{}', output: exp {}, got {}".format(
            #     case["label"], case["output"], output
            # )
        except Exception as e:
            assert type(e) == case["ex"], "case '{}', ex: exp {}, got {}".format(
                case["label"], case["ex"], type(e)
            )


def test_eq():
    cases = [
        {
            "label": "simple eq",
            "init": {
                "obstacle_str": "..........#......#......#...........",
                "bounds": ((0, 0), (6, 6)),
            },
            "input": {
                "obstacle_str": "..........#......#......#...........",
                "bounds": ((0, 0), (6, 6)),
            },
            "output": True,
            "ex": None,
        },
        {
            "label": "simple neq",
            "init": {
                "obstacle_str": "..........#......#......#...........",
                "bounds": ((0, 0), (6, 6)),
            },
            "input": {
                "obstacle_str": "#...",
                "bounds": ((0, 0), (2, 2)),
            },
            "output": False,
            "ex": None,
        },
        {
            "label": "neq content with matching bounds",
            "init": {
                "obstacle_str": ".........#......#......#............",
                "bounds": ((0, 0), (6, 6)),
            },
            "input": {
                "obstacle_str": "..........###....#......#...........",
                "bounds": ((0, 0), (6, 6)),
            },
            "output": False,
            "ex": None,
        },
        {
            "label": "eq content with mismatching bounds",
            "init": {
                "obstacle_str": ".........#......#......#............",
                "bounds": ((0, 0), (9, 4)),
            },
            "input": {
                "obstacle_str": ".........#......#......#............",
                "bounds": ((0, 0), (6, 6)),
            },
            "output": False,
            "ex": None,
        },
    ]
    for case in cases:
        try:
            obj = Map2d(**case["init"])
            output = obj == Map2d(**case["input"])
            assert output == case["output"], "case '{}', output: exp {}, got {}".format(
                case["label"], case["output"], output
            )
        except Exception as e:
            assert type(e) == case["ex"], "case '{}', ex: exp {}, got {}".format(
                case["label"], case["ex"], type(e)
            )


def test_translate_point():
    cases = [
        {
            "label": "simple",
            "init": {
                "obstacle_str": "..........#......#......#...........",
                "bounds": ((0, 0), (6, 6)),
            },
            "input": {"point": (2, 2)},
            "output": 14,
            "ex": None,
        },
        {
            "label": "rectangle",
            "init": {
                "obstacle_str": ".........#......#......#............",
                "bounds": ((0, 0), (9, 4)),
            },
            "input": {"point": (2, 2)},
            "output": 20,
            "ex": None,
        },
        {
            "label": "rectangle++",
            "init": {
                "obstacle_str": ".........#......#......#............",
                "bounds": ((0, 0), (9, 4)),
            },
            "input": {"point": (4, 2)},
            "output": 22,
            "ex": None,
        },
    ]
    for case in cases:
        try:
            obj = Map2d(**case["init"])
            output = obj.translate_point(**case["input"])
            assert output == case["output"], "case '{}', output: exp {}, got {}".format(
                case["label"], case["output"], output
            )
        except Exception as e:
            assert type(e) == case["ex"], "case '{}', ex: exp {}, got {}".format(
                case["label"], case["ex"], type(e)
            )


def test_translate_index():
    cases = [
        {
            "label": "simple",
            "init": {
                "obstacle_str": "..........#......#......#...........",
                "bounds": ((0, 0), (6, 6)),
            },
            "input": {"index": 14},
            "output": (2, 2),
            "ex": None,
        },
        {
            "label": "rectangle",
            "init": {
                "obstacle_str": ".........#......#......#............",
                "bounds": ((0, 0), (9, 4)),
            },
            "input": {"index": 20},
            "output": (2, 2),
            "ex": None,
        },
        {
            "label": "rectangle++",
            "init": {
                "obstacle_str": ".........#......#......#............",
                "bounds": ((0, 0), (9, 4)),
            },
            "input": {"index": 22},
            "output": (4, 2),
            "ex": None,
        },
    ]
    for case in cases:
        try:
            obj = Map2d(**case["init"])
            output = obj.translate_index(**case["input"])
            assert output == case["output"], "case '{}', output: exp {}, got {}".format(
                case["label"], case["output"], output
            )
        except Exception as e:
            assert type(e) == case["ex"], "case '{}', ex: exp {}, got {}".format(
                case["label"], case["ex"], type(e)
            )


def test_in_bounds_point():
    cases = [
        {
            "label": "simple",
            "init": {
                "obstacle_str": "..........#......#......#...........",
                "bounds": ((0, 0), (6, 6)),
            },
            "input": {"point": (1, 1)},
            "output": True,
            "ex": None,
        },
        {
            "label": "rectangle",
            "init": {
                "obstacle_str": ".........#......#......#............",
                "bounds": ((0, 0), (9, 4)),
            },
            "input": {"point": (8, 1)},
            "output": True,
            "ex": None,
        },
        {
            "label": "edge",
            "init": {
                "obstacle_str": ".........#......#......#............",
                "bounds": ((0, 0), (9, 4)),
            },
            "input": {"point": (0, 0)},
            "output": True,
            "ex": None,
        },
        {
            "label": "edge_out",
            "init": {
                "obstacle_str": ".........#......#......#............",
                "bounds": ((0, 0), (9, 4)),
            },
            "input": {"point": (0, 4)},
            "output": False,
            "ex": None,
        },
        {
            "label": "out",
            "init": {
                "obstacle_str": ".........#......#......#............",
                "bounds": ((0, 0), (9, 4)),
            },
            "input": {"point": (10, 6)},
            "output": False,
            "ex": None,
        },
        {
            "label": "partially out",
            "init": {
                "obstacle_str": ".........#......#......#............",
                "bounds": ((0, 0), (9, 4)),
            },
            "input": {"point": (5, 6)},
            "output": False,
            "ex": None,
        },
        {
            "label": "out negative",
            "init": {
                "obstacle_str": ".........#......#......#............",
                "bounds": ((0, 0), (9, 4)),
            },
            "input": {"point": (-1, -1)},
            "output": False,
            "ex": None,
        },
    ]
    for case in cases:
        try:
            obj = Map2d(**case["init"])
            output = obj.in_bounds_point(**case["input"])
            assert output == case["output"], "case '{}', output: exp {}, got {}".format(
                case["label"], case["output"], output
            )
        except Exception as e:
            assert type(e) == case["ex"], "case '{}', ex: exp {}, got {}".format(
                case["label"], case["ex"], type(e)
            )


def test_rotate_clockwise():
    cases = [
        {
            "label": "simple",
            "init": {
                "obstacle_str": "..........#......#......#........................",
                "bounds": ((0, 0), (7, 7)),
            },
            "output": """
.......
.......
.......
...###.
.......
.......
.......
""",
            "ex": None,
        },
        {
            "label": "simple_rect",
            "init": {
                "obstacle_str": "..........#......#......#..........",
                "bounds": ((0, 0), (7, 5)),
            },
            "output": """
.....
.....
.....
.###.
.....
.....
.....
""",
            "ex": None,
        },
    ]
    for case in cases:
        try:
            obj = Map2d(**case["init"])
            output = obj.rotate_clockwise()
            assert output.debug_draw() == case["output"], (
                "case '{}', output: exp {}, got {}".format(
                    case["label"], case["output"], output
                )
            )
        except Exception as e:
            assert type(e) == case["ex"], "case '{}', ex: exp {}, got {}".format(
                case["label"], case["ex"], type(e)
            )


def test_flip_vertically():
    cases = [
        {
            "label": "simple",
            "init": {
                "obstacle_str": "........#.......#.......#........................",
                "bounds": ((0, 0), (7, 7)),
            },
            "output": """
.......
.....#.
....#..
...#...
.......
.......
.......
""",
            "ex": None,
        },
    ]
    for case in cases:
        try:
            obj = Map2d(**case["init"])
            output = obj.flip_vertically()
            assert output.debug_draw() == case["output"], (
                "case '{}', output: exp {}, got {}".format(
                    case["label"], case["output"], output
                )
            )
        except Exception as e:
            assert type(e) == case["ex"], "case '{}', ex: exp {}, got {}".format(
                case["label"], case["ex"], type(e)
            )


def test_join_maps_left_right():
    cases = [
        {
            "label": "simple",
            "init1": {
                "obstacle_str": "...#.....#.#...#...#..#####..#...#..#...#.",
                "bounds": ((0, 0), (7, 6)),
            },
            "init2": {
                "obstacle_str": ".####...#...#..####...#...#..#...#..####..",
                "bounds": ((0, 0), (7, 6)),
            },
            "output": """
...#....####..
..#.#...#...#.
.#...#..####..
.#####..#...#.
.#...#..#...#.
.#...#..####..
""",
            "ex": None,
        },
        {
            "label": "incompatible_lenghts",
            "init1": {
                "obstacle_str": "...#.....#.#...#...#..#####..#...#..#...#........",
                "bounds": ((0, 0), (7, 7)),
            },
            "init2": {
                "obstacle_str": ".####...#...#..####...#...#..#...#..####..",
                "bounds": ((0, 0), (7, 6)),
            },
            "output": """""",
            "ex": ValueError,
        },
    ]
    for case in cases:
        try:
            obj1 = Map2d(**case["init1"])
            obj2 = Map2d(**case["init2"])
            output = Map2d.join_maps_left_right(obj1, obj2)
            assert output.debug_draw() == case["output"], (
                "case '{}', output: exp {}, got {}".format(
                    case["label"], case["output"], output
                )
            )
        except Exception as e:
            assert type(e) == case["ex"], "case '{}', ex: exp {}, got {}".format(
                case["label"], case["ex"], type(e)
            )


def test_join_maps_top_bottom():
    cases = [
        {
            "label": "simple",
            "init1": {
                "obstacle_str": "...#.....#.#...#...#..#####..#...#..#...#........",
                "bounds": ((0, 0), (7, 7)),
            },
            "init2": {
                "obstacle_str": ".####...#...#..####...#...#..#...#..####..",
                "bounds": ((0, 0), (7, 6)),
            },
            "output": """
...#...
..#.#..
.#...#.
.#####.
.#...#.
.#...#.
.......
.####..
.#...#.
.####..
.#...#.
.#...#.
.####..
""",
            "ex": None,
        },
    ]
    for case in cases:
        try:
            obj1 = Map2d(**case["init1"])
            obj2 = Map2d(**case["init2"])
            output = Map2d.join_maps_top_bottom(obj1, obj2)
            assert output.debug_draw() == case["output"], (
                "case '{}', output: exp {}, got {}".format(
                    case["label"], case["output"], output
                )
            )
        except Exception as e:
            assert type(e) == case["ex"], "case '{}', ex: exp {}, got {}".format(
                case["label"], case["ex"], type(e)
            )


def test_trim_edges():
    cases = [
        {
            "label": "simple",
            "init": {
                "obstacle_str": "..........#......#......#........................",
                "bounds": ((0, 0), (7, 7)),
            },
            "output": """
..#..
..#..
..#..
.....
.....
""",
            "ex": None,
        },
    ]
    for case in cases:
        try:
            obj = Map2d(**case["init"])
            output = obj.trim_edges()
            assert output.debug_draw() == case["output"], (
                "case '{}', output: exp {}, got {}".format(
                    case["label"], case["output"], output
                )
            )
        except Exception as e:
            assert type(e) == case["ex"], "case '{}', ex: exp {}, got {}".format(
                case["label"], case["ex"], type(e)
            )


def test_nearby_points():
    cases = [
        {
            "label": "simple",
            "init": {
                "obstacle_str": "..........#......#......#...........",
                "bounds": ((0, 0), (6, 6)),
            },
            "input": {"point": (1, 1)},
            "output": [(0, 1), (1, 0), (1, 2), (2, 1)],
            "ex": None,
        },
        {
            "label": "rectangle",
            "init": {
                "obstacle_str": ".........#......#......#............",
                "bounds": ((0, 0), (9, 4)),
            },
            "input": {"point": (7, 1)},
            "output": [(6, 1), (7, 0), (7, 2), (8, 1)],
            "ex": None,
        },
        {
            "label": "edge",
            "init": {
                "obstacle_str": ".........#......#......#............",
                "bounds": ((0, 0), (9, 4)),
            },
            "input": {"point": (0, 0)},
            "output": [(0, 1), (1, 0)],
            "ex": None,
        },
        {
            "label": "edge_out",
            "init": {
                "obstacle_str": ".........#......#......#............",
                "bounds": ((0, 0), (9, 4)),
            },
            "input": {"point": (0, 4)},
            "output": [(0, 3)],
            "ex": None,
        },
        {
            "label": "out",
            "init": {
                "obstacle_str": ".........#......#......#............",
                "bounds": ((0, 0), (9, 4)),
            },
            "input": {"point": (10, 6)},
            "output": [],
            "ex": None,
        },
        {
            "label": "partially out",
            "init": {
                "obstacle_str": ".........#......#......#............",
                "bounds": ((0, 0), (9, 4)),
            },
            "input": {"point": (5, 6)},
            "output": [],
            "ex": None,
        },
        {
            "label": "out negative",
            "init": {
                "obstacle_str": ".........#......#......#............",
                "bounds": ((0, 0), (9, 4)),
            },
            "input": {"point": (-1, -1)},
            "output": [],
            "ex": None,
        },
    ]
    for case in cases:
        try:
            obj = Map2d(**case["init"])
            output = obj.nearby_points(**case["input"])
            assert set(output) == set(case["output"]), (
                "case '{}', output: exp {}, got {}".format(
                    case["label"], case["output"], output
                )
            )
        except Exception as e:
            assert type(e) == case["ex"], "case '{}', ex: exp {}, got {}".format(
                case["label"], case["ex"], type(e)
            )


def test_debug_draw_unflooded():
    cases = [
        {
            "label": "simple",
            "init": {
                "obstacle_str": "..........#......#......#........................",
                "bounds": ((0, 0), (7, 7)),
            },
            "output": """
.......
...#...
...#...
...#...
.......
.......
.......
""",
            "ex": None,
        },
    ]
    for case in cases:
        try:
            obj = Map2d(**case["init"])
            output = obj.debug_draw()
            assert output == case["output"], "case '{}', output: exp {}, got {}".format(
                case["label"], case["output"], output
            )
        except Exception as e:
            assert type(e) == case["ex"], "case '{}', ex: exp {}, got {}".format(
                case["label"], case["ex"], type(e)
            )


def test_debug_draw_flooded():
    cases = [
        {
            "label": "small",
            "init": {"obstacles": [(3, 1), (3, 2), (3, 3)], "bounds": ((0, 0), (7, 7))},
            "input": {"starting_point": (2, 2)},
            "output": """
4323456
321#567
210#678
321#567
4323456
5434567
6545678
""",
            "ex": None,
        },
        {
            "label": "big",
            "init": {
                "obstacles": [(3, 1), (3, 2), (3, 3)],
                "bounds": ((0, 0), (31, 31)),
            },
            "input": {"starting_point": (2, 2)},
            "output": """
4323456789abcdefghijklmnopqrstu
321#56789abcdefghijklmnopqrstuv
210#6789abcdefghijklmnopqrstuvw
321#56789abcdefghijklmnopqrstuv
4323456789abcdefghijklmnopqrstu
543456789abcdefghijklmnopqrstuv
65456789abcdefghijklmnopqrstuvw
7656789abcdefghijklmnopqrstuvwx
876789abcdefghijklmnopqrstuvwxy
98789abcdefghijklmnopqrstuvwxyz
a989abcdefghijklmnopqrstuvwxyz+
ba9abcdefghijklmnopqrstuvwxyz++
cbabcdefghijklmnopqrstuvwxyz+++
dcbcdefghijklmnopqrstuvwxyz++++
edcdefghijklmnopqrstuvwxyz+++++
fedefghijklmnopqrstuvwxyz++++++
gfefghijklmnopqrstuvwxyz+++++++
hgfghijklmnopqrstuvwxyz++++++++
ihghijklmnopqrstuvwxyz+++++++++
jihijklmnopqrstuvwxyz++++++++++
kjijklmnopqrstuvwxyz+++++++++++
lkjklmnopqrstuvwxyz++++++++++++
mlklmnopqrstuvwxyz+++++++++++++
nmlmnopqrstuvwxyz++++++++++++++
onmnopqrstuvwxyz+++++++++++++++
ponopqrstuvwxyz++++++++++++++++
qpopqrstuvwxyz+++++++++++++++++
rqpqrstuvwxyz++++++++++++++++++
srqrstuvwxyz+++++++++++++++++++
tsrstuvwxyz++++++++++++++++++++
utstuvwxyz+++++++++++++++++++++
""",
            "ex": None,
        },
        {
            "label": "big with a pocket",
            "init": {
                "obstacles": [
                    (4, 4),
                    (4, 5),
                    (4, 6),
                    (4, 7),
                    (4, 8),
                    (4, 9),
                    (4, 10),
                    (14, 4),
                    (14, 5),
                    (14, 6),
                    (14, 7),
                    (14, 8),
                    (14, 9),
                    (14, 10),
                    (5, 4),
                    (6, 4),
                    (7, 4),
                    (8, 4),
                    (9, 4),
                    (10, 4),
                    (11, 4),
                    (12, 4),
                    (13, 4),
                    (5, 10),
                    (6, 10),
                    (7, 10),
                    (8, 10),
                    (9, 10),
                    (10, 10),
                    (11, 10),
                    (12, 10),
                    (13, 10),
                ],
                "bounds": ((0, 0), (31, 31)),
            },
            "input": {"starting_point": (2, 2)},
            "output": """
4323456789abcdefghijklmnopqrstu
32123456789abcdefghijklmnopqrst
210123456789abcdefghijklmnopqrs
32123456789abcdefghijklmnopqrst
4323###########fghijklmnopqrstu
5434#.........#ghijklmnopqrstuv
6545#.........#hijklmnopqrstuvw
7656#.........#ijklmnopqrstuvwx
8767#.........#jklmnopqrstuvwxy
9878#.........#klmnopqrstuvwxyz
a989###########lmnopqrstuvwxyz+
ba9abcdefghijklmnopqrstuvwxyz++
cbabcdefghijklmnopqrstuvwxyz+++
dcbcdefghijklmnopqrstuvwxyz++++
edcdefghijklmnopqrstuvwxyz+++++
fedefghijklmnopqrstuvwxyz++++++
gfefghijklmnopqrstuvwxyz+++++++
hgfghijklmnopqrstuvwxyz++++++++
ihghijklmnopqrstuvwxyz+++++++++
jihijklmnopqrstuvwxyz++++++++++
kjijklmnopqrstuvwxyz+++++++++++
lkjklmnopqrstuvwxyz++++++++++++
mlklmnopqrstuvwxyz+++++++++++++
nmlmnopqrstuvwxyz++++++++++++++
onmnopqrstuvwxyz+++++++++++++++
ponopqrstuvwxyz++++++++++++++++
qpopqrstuvwxyz+++++++++++++++++
rqpqrstuvwxyz++++++++++++++++++
srqrstuvwxyz+++++++++++++++++++
tsrstuvwxyz++++++++++++++++++++
utstuvwxyz+++++++++++++++++++++
""",
            "ex": None,
        },
    ]
    for case in cases:
        try:
            obj = Map2d.from_obstacle_list(**case["init"])
            obj.flood(**case["input"])
            output = obj.debug_draw()
            assert output == case["output"], "case '{}', output: exp {}, got {}".format(
                case["label"], case["output"], output
            )
        except Exception as e:
            assert type(e) == case["ex"], "case '{}', ex: exp {}, got {}".format(
                case["label"], case["ex"], type(e)
            )


def test_flood():
    cases = [
        {
            "label": "simple",
            "init": {"obstacles": [(3, 1), (3, 2), (3, 3)], "bounds": ((0, 0), (7, 7))},
            "input": {"starting_point": (2, 2)},
            "check": {"point": (3, 4)},
            "output": 3,
            "ex": None,
        },
        {
            "label": "obstacle",
            "init": {"obstacles": [(3, 1), (3, 2), (3, 3)], "bounds": ((0, 0), (7, 7))},
            "input": {"starting_point": (2, 2)},
            "check": {"point": (3, 2)},
            "output": -1,
            "ex": None,
        },
        {
            "label": "pocket",
            "init": {
                "obstacles": [
                    (4, 4),
                    (4, 5),
                    (4, 6),
                    (4, 7),
                    (4, 8),
                    (4, 9),
                    (4, 10),
                    (14, 4),
                    (14, 5),
                    (14, 6),
                    (14, 7),
                    (14, 8),
                    (14, 9),
                    (14, 10),
                    (5, 4),
                    (6, 4),
                    (7, 4),
                    (8, 4),
                    (9, 4),
                    (10, 4),
                    (11, 4),
                    (12, 4),
                    (13, 4),
                    (5, 10),
                    (6, 10),
                    (7, 10),
                    (8, 10),
                    (9, 10),
                    (10, 10),
                    (11, 10),
                    (12, 10),
                    (13, 10),
                ],
                "bounds": ((0, 0), (31, 31)),
            },
            "input": {"starting_point": (2, 2)},
            "check": {"point": (5, 5)},
            "output": -1,
            "ex": None,
        },
        {
            "label": "inside_pocket",
            "init": {
                "obstacles": [
                    (4, 4),
                    (4, 5),
                    (4, 6),
                    (4, 7),
                    (4, 8),
                    (4, 9),
                    (4, 10),
                    (14, 4),
                    (14, 5),
                    (14, 6),
                    (14, 7),
                    (14, 8),
                    (14, 9),
                    (14, 10),
                    (5, 4),
                    (6, 4),
                    (7, 4),
                    (8, 4),
                    (9, 4),
                    (10, 4),
                    (11, 4),
                    (12, 4),
                    (13, 4),
                    (5, 10),
                    (6, 10),
                    (7, 10),
                    (8, 10),
                    (9, 10),
                    (10, 10),
                    (11, 10),
                    (12, 10),
                    (13, 10),
                ],
                "bounds": ((0, 0), (31, 31)),
            },
            "input": {"starting_point": (9, 7)},
            "check": {"point": (5, 5)},
            "output": 6,
            "ex": None,
        },
    ]
    for case in cases:
        try:
            obj = Map2d.from_obstacle_list(**case["init"])
            obj.flood(**case["input"])
            output = obj.get_flooded_point(**case["check"])
            assert output == case["output"], "case '{}', output: exp {}, got {}".format(
                case["label"], case["output"], output
            )
        except Exception as e:
            assert type(e) == case["ex"], "case '{}', ex: exp {}, got {}".format(
                case["label"], case["ex"], type(e)
            )


def test_get_flood_max_indexes():
    cases = [
        {
            "label": "simple",
            "init": {"obstacles": [(3, 1), (3, 2), (3, 3)], "bounds": ((0, 0), (7, 7))},
            "input": {"starting_point": (2, 2)},
            "output": ([(6, 2), (6, 6)], 8),
            "ex": None,
        },
        {
            "label": "pocket",
            "init": {
                "obstacles": [
                    (4, 4),
                    (4, 5),
                    (4, 6),
                    (4, 7),
                    (4, 8),
                    (4, 9),
                    (4, 10),
                    (14, 4),
                    (14, 5),
                    (14, 6),
                    (14, 7),
                    (14, 8),
                    (14, 9),
                    (14, 10),
                    (5, 4),
                    (6, 4),
                    (7, 4),
                    (8, 4),
                    (9, 4),
                    (10, 4),
                    (11, 4),
                    (12, 4),
                    (13, 4),
                    (5, 10),
                    (6, 10),
                    (7, 10),
                    (8, 10),
                    (9, 10),
                    (10, 10),
                    (11, 10),
                    (12, 10),
                    (13, 10),
                ],
                "bounds": ((0, 0), (31, 31)),
            },
            "input": {"starting_point": (2, 2)},
            "output": ([(30, 30)], 56),
            "ex": None,
        },
        {
            "label": "inside_pocket",
            "init": {
                "obstacles": [
                    (4, 4),
                    (4, 5),
                    (4, 6),
                    (4, 7),
                    (4, 8),
                    (4, 9),
                    (4, 10),
                    (14, 4),
                    (14, 5),
                    (14, 6),
                    (14, 7),
                    (14, 8),
                    (14, 9),
                    (14, 10),
                    (5, 4),
                    (6, 4),
                    (7, 4),
                    (8, 4),
                    (9, 4),
                    (10, 4),
                    (11, 4),
                    (12, 4),
                    (13, 4),
                    (5, 10),
                    (6, 10),
                    (7, 10),
                    (8, 10),
                    (9, 10),
                    (10, 10),
                    (11, 10),
                    (12, 10),
                    (13, 10),
                ],
                "bounds": ((0, 0), (31, 31)),
            },
            "input": {"starting_point": (9, 7)},
            "output": (
                [
                    (5, 5),
                    (5, 9),
                    (13, 5),
                    (13, 9),
                ],
                6,
            ),
            "ex": None,
        },
    ]
    for case in cases:
        try:
            obj = Map2d.from_obstacle_list(**case["init"])
            obj.flood(**case["input"])
            output = obj.get_flood_max_indexes()
            assert output[1] == case["output"][1], (
                "case '{}', output: exp {}, got {}".format(
                    case["label"], case["output"], output
                )
            )
            assert output[0].sort() == case["output"][0].sort(), (
                "case '{}', output: exp {}, got {}".format(
                    case["label"], case["output"], output
                )
            )
        except Exception as e:
            assert type(e) == case["ex"], "case '{}', ex: exp {}, got {}".format(
                case["label"], case["ex"], type(e)
            )


def test_empties_to_obstacles():
    cases = [
        {
            "label": "simple",
            "input": {"empties": [(3, 1), (3, 2), (3, 3)], "bounds": ((0, 0), (7, 7))},
            "output": [
                (0, 0),
                (0, 1),
                (0, 2),
                (0, 3),
                (0, 4),
                (0, 5),
                (0, 6),
                (1, 0),
                (1, 1),
                (1, 2),
                (1, 3),
                (1, 4),
                (1, 5),
                (1, 6),
                (2, 0),
                (2, 1),
                (2, 2),
                (2, 3),
                (2, 4),
                (2, 5),
                (2, 6),
                (3, 0),
                (3, 4),
                (3, 5),
                (3, 6),
                (4, 0),
                (4, 1),
                (4, 2),
                (4, 3),
                (4, 4),
                (4, 5),
                (4, 6),
                (5, 0),
                (5, 1),
                (5, 2),
                (5, 3),
                (5, 4),
                (5, 5),
                (5, 6),
                (6, 0),
                (6, 1),
                (6, 2),
                (6, 3),
                (6, 4),
                (6, 5),
                (6, 6),
            ],
            "ex": None,
        },
    ]
    for case in cases:
        try:
            output = Map2d.empties_to_obstacles(**case["input"])
            assert output == case["output"], "case '{}', output: exp {}, got {}".format(
                case["label"], case["output"], output
            )
        except Exception as e:
            assert type(e) == case["ex"], "case '{}', ex: exp {}, got {}".format(
                case["label"], case["ex"], type(e)
            )


def test_invert_obstacles():
    cases = [
        {
            "label": "simple",
            "init": {
                "obstacle_str": "..........#......#......#........................",
                "bounds": ((0, 0), (7, 7)),
            },
            "output": """
#######
###.###
###.###
###.###
#######
#######
#######
""",
            "ex": None,
        },
    ]
    for case in cases:
        try:
            obj = Map2d(**case["init"])
            obj.invert_obstacles()
            output = obj.debug_draw()
            assert output == case["output"], "case '{}', output: exp {}, got {}".format(
                case["label"], case["output"], output
            )
        except Exception as e:
            assert type(e) == case["ex"], "case '{}', ex: exp {}, got {}".format(
                case["label"], case["ex"], type(e)
            )


def test_invert_point():
    cases = [
        {
            "label": "simple",
            "init": {
                "obstacle_str": "..........#......#......#........................",
                "bounds": ((0, 0), (7, 7)),
            },
            "input": {"point": (2, 5)},
            "output": """
.......
...#...
...#...
...#...
.......
..#....
.......
""",
            "ex": None,
        },
        {
            "label": "simple2",
            "init": {
                "obstacle_str": "..........#......#......#........................",
                "bounds": ((0, 0), (7, 7)),
            },
            "input": {"point": (3, 1)},
            "output": """
.......
.......
...#...
...#...
.......
.......
.......
""",
            "ex": None,
        },
    ]
    for case in cases:
        try:
            obj = Map2d(**case["init"])
            obj.invert_point(**case["input"])
            output = obj.debug_draw()
            assert output == case["output"], "case '{}', output: exp {}, got {}".format(
                case["label"], case["output"], output
            )
        except Exception as e:
            assert type(e) == case["ex"], "case '{}', ex: exp {}, got {}".format(
                case["label"], case["ex"], type(e)
            )


def test_find_reflection_axes():
    cases = [
        {
            "label": "2023, day13, test1",
            "init": {
                "obstacle_str": "#.##..##...#.##.#.##......###......#..#.##.#...##..##.#.#.##.#.",
                "bounds": ((0, 0), (9, 7)),
            },
            "output": (None, 5),
            "ex": None,
        },
        {
            "label": "2023, day13, test2",
            "init": {
                "obstacle_str": "#...##..##....#..#..##..########.##.#####.##...##..####....#..#",
                "bounds": ((0, 0), (9, 7)),
            },
            "output": (4, None),
            "ex": None,
        },
    ]
    for case in cases:
        try:
            obj = Map2d(**case["init"])
            output = obj.find_reflection_axes()
            assert output == case["output"], "case '{}', output: exp {}, got {}".format(
                case["label"], case["output"], output
            )
        except Exception as e:
            assert type(e) == case["ex"], "case '{}', ex: exp {}, got {}".format(
                case["label"], case["ex"], type(e)
            )


def test_pipe_map_init():
    cases = [
        {
            "label": "simple",
            "init": {
                "pipes": {
                    (1, 4): PipeType.TopDown,
                    (1, 3): PipeType.TopDown,
                    (1, 2): PipeType.TopDown,
                    (1, 1): PipeType.RightDown,
                    (2, 1): PipeType.LeftDown,
                    (2, 2): PipeType.TopDown,
                    (2, 3): PipeType.TopRight,
                    (3, 3): PipeType.LeftRight,
                    (4, 3): PipeType.TopLeft,
                    (4, 2): PipeType.TopDown,
                    (4, 1): PipeType.LeftDown,
                    (3, 1): PipeType.TopRight,
                    (3, 0): PipeType.TopDown,
                },
                "bounds": ((0, 0), (5, 5)),
            },
            "output": """
##########.####
##########.####
##########.####
##########.####
####....##....#
####.##.#####.#
####.##.#####.#
####.##.#####.#
####.##.#####.#
####.##.#####.#
####.##.......#
####.##########
####.##########
####.##########
####.##########
""",
            "ex": None,
        },
        {
            "label": "loop",
            "init": {
                "pipes": {
                    (4, 0): PipeType.RightDown,
                    (5, 0): PipeType.LeftRight,
                    (6, 0): PipeType.LeftDown,
                    (6, 1): PipeType.TopLeft,
                    (5, 1): PipeType.RightDown,
                    (5, 2): PipeType.TopLeft,
                    (4, 2): PipeType.LeftRight,
                    (3, 2): PipeType.LeftRight,
                    (2, 2): PipeType.RightDown,
                    (2, 3): PipeType.TopLeft,
                    (1, 3): PipeType.TopRight,
                    (1, 2): PipeType.TopDown,
                    (1, 1): PipeType.RightDown,
                    (2, 1): PipeType.LeftRight,
                    (3, 1): PipeType.LeftRight,
                    (4, 1): PipeType.TopLeft,
                },
                "bounds": ((0, 0), (7, 4)),
            },
            "output": """
#####################
#############.......#
#############.#####.#
#############.#####.#
####..........##....#
####.###########.####
####.###########.####
####.##..........####
####.##.#############
####.##.#############
####....#############
#####################
""",
            "ex": None,
        },
    ]
    for case in cases:
        try:
            obj = PipeMap2d(**case["init"])
            output = obj.inner_map.debug_draw()
            assert output == case["output"], "case '{}', output: exp {}, got {}".format(
                case["label"], case["output"], output
            )
        except Exception as e:
            assert type(e) == case["ex"], "case '{}', ex: exp {}, got {}".format(
                case["label"], case["ex"], type(e)
            )


def test_pipe_map_flood():
    cases = [
        {
            "label": "simple",
            "init": {
                "pipes": {
                    (1, 4): PipeType.TopDown,
                    (1, 3): PipeType.TopDown,
                    (1, 2): PipeType.TopDown,
                    (1, 1): PipeType.RightDown,
                    (2, 1): PipeType.LeftDown,
                    (2, 2): PipeType.TopDown,
                    (2, 3): PipeType.TopRight,
                    (3, 3): PipeType.LeftRight,
                    (4, 3): PipeType.TopLeft,
                    (4, 2): PipeType.TopDown,
                    (4, 1): PipeType.LeftDown,
                    (3, 1): PipeType.TopRight,
                    (3, 0): PipeType.TopDown,
                },
                "bounds": ((0, 0), (5, 5)),
            },
            "input": {"starting_point": (1, 4)},
            "output": """
##########+####
##########+####
##########z####
##########y####
####9abc##xwvu#
####8##d#####t#
####7##e#####s#
####6##f#####r#
####5##g#####q#
####4##h#####p#
####3##ijklmno#
####2##########
####1##########
####0##########
####1##########
""",
            "ex": None,
        },
        {
            "label": "loop",
            "init": {
                "pipes": {
                    (4, 0): PipeType.RightDown,
                    (5, 0): PipeType.LeftRight,
                    (6, 0): PipeType.LeftDown,
                    (6, 1): PipeType.TopLeft,
                    (5, 1): PipeType.RightDown,
                    (5, 2): PipeType.TopLeft,
                    (4, 2): PipeType.LeftRight,
                    (3, 2): PipeType.LeftRight,
                    (2, 2): PipeType.RightDown,
                    (2, 3): PipeType.TopLeft,
                    (1, 3): PipeType.TopRight,
                    (1, 2): PipeType.TopDown,
                    (1, 1): PipeType.RightDown,
                    (2, 1): PipeType.LeftRight,
                    (3, 1): PipeType.LeftRight,
                    (4, 1): PipeType.TopLeft,
                },
                "bounds": ((0, 0), (7, 4)),
            },
            "input": {"starting_point": (1, 1)},
            "output": """
#####################
#############cdefghi#
#############b#####j#
#############a#####k#
####0123456789##onml#
####1###########n####
####2###########m####
####3##cdefghijkl####
####4##b#############
####5##a#############
####6789#############
#####################
""",
            "ex": None,
        },
    ]
    for case in cases:
        try:
            obj = PipeMap2d(**case["init"])
            obj.flood(**case["input"])
            output = obj.inner_map.debug_draw()
            assert output == case["output"], "case '{}', output: exp {}, got {}".format(
                case["label"], case["output"], output
            )
        except Exception as e:
            assert type(e) == case["ex"], "case '{}', ex: exp {}, got {}".format(
                case["label"], case["ex"], type(e)
            )


def test_pipe_map_flooded_val():
    cases = [
        {
            "label": "simple",
            "init": {
                "pipes": {
                    (1, 4): PipeType.TopDown,
                    (1, 3): PipeType.TopDown,
                    (1, 2): PipeType.TopDown,
                    (1, 1): PipeType.RightDown,
                    (2, 1): PipeType.LeftDown,
                    (2, 2): PipeType.TopDown,
                    (2, 3): PipeType.TopRight,
                    (3, 3): PipeType.LeftRight,
                    (4, 3): PipeType.TopLeft,
                    (4, 2): PipeType.TopDown,
                    (4, 1): PipeType.LeftDown,
                    (3, 1): PipeType.TopRight,
                    (3, 0): PipeType.TopDown,
                },
                "bounds": ((0, 0), (5, 5)),
            },
            "input_flood": {"starting_point": (1, 4)},
            "input": {"point": (3, 1)},
            "output": 11,
            "ex": None,
        },
        {
            "label": "loop",
            "init": {
                "pipes": {
                    (4, 0): PipeType.RightDown,
                    (5, 0): PipeType.LeftRight,
                    (6, 0): PipeType.LeftDown,
                    (6, 1): PipeType.TopLeft,
                    (5, 1): PipeType.RightDown,
                    (5, 2): PipeType.TopLeft,
                    (4, 2): PipeType.LeftRight,
                    (3, 2): PipeType.LeftRight,
                    (2, 2): PipeType.RightDown,
                    (2, 3): PipeType.TopLeft,
                    (1, 3): PipeType.TopRight,
                    (1, 2): PipeType.TopDown,
                    (1, 1): PipeType.RightDown,
                    (2, 1): PipeType.LeftRight,
                    (3, 1): PipeType.LeftRight,
                    (4, 1): PipeType.TopLeft,
                },
                "bounds": ((0, 0), (7, 4)),
            },
            "input_flood": {"starting_point": (1, 1)},
            "input": {"point": (5, 1)},
            "output": 8,
            "ex": None,
        },
    ]
    for case in cases:
        try:
            obj = PipeMap2d(**case["init"])
            obj.flood(**case["input_flood"])
            output = obj.get_flooded_point(**case["input"])
            assert output == case["output"], "case '{}', output: exp {}, got {}".format(
                case["label"], case["output"], output
            )
        except Exception as e:
            assert type(e) == case["ex"], "case '{}', ex: exp {}, got {}".format(
                case["label"], case["ex"], type(e)
            )


def test_pipe_map_flooded_val_max():
    cases = [
        {
            "label": "simple",
            "init": {
                "pipes": {
                    (1, 4): PipeType.TopDown,
                    (1, 3): PipeType.TopDown,
                    (1, 2): PipeType.TopDown,
                    (1, 1): PipeType.RightDown,
                    (2, 1): PipeType.LeftDown,
                    (2, 2): PipeType.TopDown,
                    (2, 3): PipeType.TopRight,
                    (3, 3): PipeType.LeftRight,
                    (4, 3): PipeType.TopLeft,
                    (4, 2): PipeType.TopDown,
                    (4, 1): PipeType.LeftDown,
                    (3, 1): PipeType.TopRight,
                    (3, 0): PipeType.TopDown,
                },
                "bounds": ((0, 0), (5, 5)),
            },
            "input": {"starting_point": (1, 4)},
            "output": ({(3, 0)}, 12),
            "ex": None,
        },
        {
            "label": "loop",
            "init": {
                "pipes": {
                    (4, 0): PipeType.RightDown,
                    (5, 0): PipeType.LeftRight,
                    (6, 0): PipeType.LeftDown,
                    (6, 1): PipeType.TopLeft,
                    (5, 1): PipeType.RightDown,
                    (5, 2): PipeType.TopLeft,
                    (4, 2): PipeType.LeftRight,
                    (3, 2): PipeType.LeftRight,
                    (2, 2): PipeType.RightDown,
                    (2, 3): PipeType.TopLeft,
                    (1, 3): PipeType.TopRight,
                    (1, 2): PipeType.TopDown,
                    (1, 1): PipeType.RightDown,
                    (2, 1): PipeType.LeftRight,
                    (3, 1): PipeType.LeftRight,
                    (4, 1): PipeType.TopLeft,
                },
                "bounds": ((0, 0), (7, 4)),
            },
            "input": {"starting_point": (1, 1)},
            "output": ({(5, 1)}, 8),
            "ex": None,
        },
    ]
    for case in cases:
        try:
            obj = PipeMap2d(**case["init"])
            obj.flood(**case["input"])
            output = obj.get_flood_max_indexes()
            assert output == case["output"], "case '{}', output: exp {}, got {}".format(
                case["label"], case["output"], output
            )
        except Exception as e:
            assert type(e) == case["ex"], "case '{}', ex: exp {}, got {}".format(
                case["label"], case["ex"], type(e)
            )
