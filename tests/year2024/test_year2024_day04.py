# test 2024-04

import pytest

from aoc.year2024.day04 import part1, part2


def test_part1():
    cases = [
        {
            "label": "small",
            "input": {
                "in_data": """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
"""
            },
            "output": "18",
            "ex": None,
        },
        {
            "label": "small",
            "input": {
                "in_data": """MMMSXXMASM
"""
            },
            "output": "1",
            "ex": None,
        },
    ]
    for case in cases:
        try:
            output = part1(**case["input"])
            assert str(output) == str(
                case["output"]
            ), "case '{}', output: exp {}, got {}".format(
                case["label"], case["output"], output
            )
        except Exception as e:
            assert type(e) == case["ex"], "case '{}', ex: exp {}, got {}".format(
                case["label"], case["ex"], type(e)
            )


def test_part2():
    cases = [
        {
            "label": "smaller",
            "input": {
                "in_data": """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
"""
            },
            "output": "1",
            "ex": None,
        },
        {
            "label": "small",
            "input": {
                "in_data": """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
"""
            },
            "output": "9",
            "ex": None,
        },
    ]
    for case in cases:
        try:
            output = part2(**case["input"])
            assert str(output) == str(
                case["output"]
            ), "case '{}', output: exp {}, got {}".format(
                case["label"], case["output"], output
            )
        except Exception as e:
            assert type(e) == case["ex"], "case '{}', ex: exp {}, got {}".format(
                case["label"], case["ex"], type(e)
            )
