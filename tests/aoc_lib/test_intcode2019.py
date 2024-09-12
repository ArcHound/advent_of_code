import pytest

from aoc_lib.intcode2019 import *


def test_process_program():
    cases = [
        {
            "label": "day 2, ex 1",
            "input": {"data": [1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50]},
            "data": [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50],
            "stdout": [],
            "ex": None,
        },
        {
            "label": "day 2, ex 2",
            "input": {"data": [1, 0, 0, 0, 99]},
            "data": [2, 0, 0, 0, 99],
            "stdout": [],
            "ex": None,
        },
        {
            "label": "day 2, ex 3",
            "input": {"data": [2, 3, 0, 3, 99]},
            "data": [2, 3, 0, 6, 99],
            "stdout": [],
            "ex": None,
        },
        {
            "label": "day 2, ex 4",
            "input": {"data": [2, 4, 4, 5, 99, 0]},
            "data": [2, 4, 4, 5, 99, 9801],
            "stdout": [],
            "ex": None,
        },
        {
            "label": "day 2, ex 4",
            "input": {"data": [1, 1, 1, 4, 99, 5, 6, 0, 99]},
            "data": [30, 1, 1, 4, 2, 5, 6, 0, 99],
            "stdout": [],
            "ex": None,
        },
        {
            "label": "day 5, ex 1",
            "input": {"data": [3, 0, 4, 0, 99], "stdin": [42]},
            "data": [42, 0, 4, 0, 99],
            "stdout": [42],
            "ex": None,
        },
        {
            "label": "day 5, ex 2",
            "input": {"data": [1002, 4, 3, 4, 33]},
            "data": [1002, 4, 3, 4, 99],
            "stdout": [],
            "ex": None,
        },
        {
            "label": "day 5, ex 3",
            "input": {"data": [1101, 100, -1, 4, 0]},
            "data": [1101, 100, -1, 4, 99],
            "stdout": [],
            "ex": None,
        },
        {
            "label": "day 5, ex 4 equal",
            "input": {"data": [3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], "stdin": [8]},
            "data": [3, 9, 8, 9, 10, 9, 4, 9, 99, 1, 8],
            "stdout": [1],
            "ex": None,
        },
        {
            "label": "day 5, ex 4 not equal",
            "input": {"data": [3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], "stdin": [19]},
            "data": [3, 9, 8, 9, 10, 9, 4, 9, 99, 0, 8],
            "stdout": [0],
            "ex": None,
        },
        {
            "label": "day 5, ex 4 not less than",
            "input": {"data": [3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], "stdin": [8]},
            "data": [3, 9, 7, 9, 10, 9, 4, 9, 99, 0, 8],
            "stdout": [0],
            "ex": None,
        },
        {
            "label": "day 5, ex 4 less than",
            "input": {"data": [3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], "stdin": [4]},
            "data": [3, 9, 7, 9, 10, 9, 4, 9, 99, 1, 8],
            "stdout": [1],
            "ex": None,
        },
        {
            "label": "day 5, ex 4 immediate equal",
            "input": {"data": [3, 3, 1108, -1, 8, 3, 4, 3, 99], "stdin": [8]},
            "data": [3, 3, 1108, 1, 8, 3, 4, 3, 99],
            "stdout": [1],
            "ex": None,
        },
        {
            "label": "day 5, ex 5 position jump",
            "input": {
                "data": [3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9],
                "stdin": [8],
            },
            "stdout": [1],
            "ex": None,
        },
        {
            "label": "day 5, ex 5 immediate jump",
            "input": {
                "data": [3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1],
                "stdin": [8],
            },
            "stdout": [1],
            "ex": None,
        },
    ]
    for case in cases:
        try:
            computer = Intcode2019()
            computer.run_program(**case["input"])
            data = computer.data
            if "data" in case:
                assert data == case["data"], "case '{}', output: exp {}, got {}".format(
                    case["label"], case["data"], data
                )
            stdout = computer.get_list_output()
            if "stdout" in case:
                assert (
                    stdout == case["stdout"]
                ), "case '{}', output: exp {}, got {}".format(
                    case["label"], case["stdout"], stdout
                )
        except Exception as e:
            assert type(e) == case["ex"], "case '{}', ex: exp {}, got {}".format(
                case["label"], case["ex"], type(e)
            )
