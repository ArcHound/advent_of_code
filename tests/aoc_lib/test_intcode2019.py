import pytest

from aoc_lib.intcode2019 import *


def test_run_program():
    cases = [
        {
            "label": "day 2, ex 1",
            "input": {"data": [1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50]},
            "data": {
                0: 3500,
                1: 9,
                2: 10,
                3: 70,
                4: 2,
                5: 3,
                6: 11,
                7: 0,
                8: 99,
                9: 30,
                10: 40,
                11: 50,
            },
            "stdout": [],
            "ex": None,
        },
        {
            "label": "day 2, ex 2",
            "input": {"data": [1, 0, 0, 0, 99]},
            "data": {0: 2, 1: 0, 2: 0, 3: 0, 4: 99},
            "stdout": [],
            "ex": None,
        },
        {
            "label": "day 2, ex 3",
            "input": {"data": [2, 3, 0, 3, 99]},
            "data": {0: 2, 1: 3, 2: 0, 3: 6, 4: 99},
            "stdout": [],
            "ex": None,
        },
        {
            "label": "day 2, ex 4",
            "input": {"data": [2, 4, 4, 5, 99, 0]},
            "data": {0: 2, 1: 4, 2: 4, 3: 5, 4: 99, 5: 9801},
            "stdout": [],
            "ex": None,
        },
        {
            "label": "day 2, ex 4",
            "input": {"data": [1, 1, 1, 4, 99, 5, 6, 0, 99]},
            "data": {0: 30, 1: 1, 2: 1, 3: 4, 4: 2, 5: 5, 6: 6, 7: 0, 8: 99},
            "stdout": [],
            "ex": None,
        },
        {
            "label": "day 5, ex 1",
            "input": {"data": [3, 0, 4, 0, 99], "stdin": [42]},
            "data": {0: 42, 1: 0, 2: 4, 3: 0, 4: 99},
            "stdout": [42],
            "ex": None,
        },
        {
            "label": "day 5, ex 2",
            "input": {"data": [1002, 4, 3, 4, 33]},
            "data": {0: 1002, 1: 4, 2: 3, 3: 4, 4: 99},
            "stdout": [],
            "ex": None,
        },
        {
            "label": "day 5, ex 3",
            "input": {"data": [1101, 100, -1, 4, 0]},
            "data": {0: 1101, 1: 100, 2: -1, 3: 4, 4: 99},
            "stdout": [],
            "ex": None,
        },
        {
            "label": "day 5, ex 4 equal",
            "input": {"data": [3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], "stdin": [8]},
            "stdout": [1],
            "ex": None,
        },
        {
            "label": "day 5, ex 4 not equal",
            "input": {"data": [3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], "stdin": [19]},
            "stdout": [0],
            "ex": None,
        },
        {
            "label": "day 5, ex 4 not less than",
            "input": {"data": [3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], "stdin": [8]},
            "stdout": [0],
            "ex": None,
        },
        {
            "label": "day 5, ex 4 less than",
            "input": {"data": [3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], "stdin": [4]},
            "stdout": [1],
            "ex": None,
        },
        {
            "label": "day 5, ex 4 immediate equal",
            "input": {"data": [3, 3, 1108, -1, 8, 3, 4, 3, 99], "stdin": [8]},
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
        {
            "label": "day 9, quine",
            "input": {
                "data": [
                    109,
                    1,
                    204,
                    -1,
                    1001,
                    100,
                    1,
                    100,
                    1008,
                    100,
                    16,
                    101,
                    1006,
                    101,
                    0,
                    99,
                ],
                "stdin": [],
            },
            "stdout": [
                109,
                1,
                204,
                -1,
                1001,
                100,
                1,
                100,
                1008,
                100,
                16,
                101,
                1006,
                101,
                0,
                99,
            ],
            "ex": None,
        },
        {
            "label": "day 9, mult",
            "input": {
                "data": [1102, 34915192, 34915192, 7, 4, 7, 99, 0],
                "stdin": [],
            },
            "stdout": [1219070632396864],
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
