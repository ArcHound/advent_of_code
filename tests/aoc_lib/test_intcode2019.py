import pytest

from aoc_lib.intcode2019 import *


def test_process_program():
    cases = [
        {
            "label": "day 2, ex 1",
            "input": {"data": [1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50]},
            "output": [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50],
            "ex": None,
        },
        {
            "label": "day 2, ex 2",
            "input": {"data": [1, 0, 0, 0, 99]},
            "output": [2, 0, 0, 0, 99],
            "ex": None,
        },
        {
            "label": "day 2, ex 3",
            "input": {"data": [2, 3, 0, 3, 99]},
            "output": [2, 3, 0, 6, 99],
            "ex": None,
        },
        {
            "label": "day 2, ex 4",
            "input": {"data": [2, 4, 4, 5, 99, 0]},
            "output": [2, 4, 4, 5, 99, 9801],
            "ex": None,
        },
        {
            "label": "day 2, ex 4",
            "input": {"data": [1, 1, 1, 4, 99, 5, 6, 0, 99]},
            "output": [30, 1, 1, 4, 2, 5, 6, 0, 99],
            "ex": None,
        },
    ]
    computer = Intcode2019()
    for case in cases:
        try:
            computer.process_program(**case["input"])
            output = computer.data
            assert output == case["output"], "case '{}', output: exp {}, got {}".format(
                case["label"], case["output"], output
            )
        except Exception as e:
            assert type(e) == case["ex"], "case '{}', ex: exp {}, got {}".format(
                case["label"], case["ex"], type(e)
            )
