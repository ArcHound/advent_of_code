import datetime

# vim: nomodeline
import json
from unittest.mock import patch, mock_open
import pytest

from aoc_lib.num_theory import *


def test_primes_under_n():
    cases = [
        {
            "label": "two",
            "input": {"n": 2},
            "output": [2],
            "ex": None,
        },
        {
            "label": "three",
            "input": {"n": 3},
            "output": [2, 3],
            "ex": None,
        },
        {
            "label": "ten",
            "input": {"n": 10},
            "output": [2, 3, 5, 7],
            "ex": None,
        },
        {
            "label": "hundred",
            "input": {"n": 100},
            "output": [
                2,
                3,
                5,
                7,
                11,
                13,
                17,
                19,
                23,
                29,
                31,
                37,
                41,
                43,
                47,
                53,
                59,
                61,
                67,
                71,
                73,
                79,
                83,
                89,
                97,
            ],
            "ex": None,
        },
    ]
    for case in cases:
        try:
            output = primes_under_n(**case["input"])
            assert output == case["output"], "case '{}', output: exp {}, got {}".format(
                case["label"], case["output"], output
            )
        except Exception as e:
            assert type(e) == case["ex"], "case '{}', ex: exp {}, got {}".format(
                case["label"], case["ex"], type(e)
            )


def test_factorize():
    cases = [
        {
            "label": "two",
            "input": {"n": 2},
            "output": {2: 1},
            "ex": None,
        },
        {
            "label": "three",
            "input": {"n": 3},
            "output": {3: 1},
            "ex": None,
        },
        {
            "label": "ten",
            "input": {"n": 10},
            "output": {2: 1, 5: 1},
            "ex": None,
        },
        {
            "label": "sixteen",
            "input": {"n": 16},
            "output": {2: 4},
            "ex": None,
        },
        {
            "label": "hundred",
            "input": {"n": 100},
            "output": {2: 2, 5: 2},
            "ex": None,
        },
        {
            "label": "1013",
            "input": {"n": 1013},
            "output": {1013: 1},
            "ex": None,
        },
        {
            "label": "381024",
            "input": {"n": 381024},
            "output": {2: 5, 3: 5, 7: 2},
            "ex": None,
        },
    ]
    for case in cases:
        try:
            output = factorize(**case["input"])
            assert output == case["output"], "case '{}', output: exp {}, got {}".format(
                case["label"], case["output"], output
            )
        except Exception as e:
            assert type(e) == case["ex"], "case '{}', ex: exp {}, got {}".format(
                case["label"], case["ex"], type(e)
            )


def test_sum_of_divisors():
    cases = [
        {
            "label": "two",
            "input": {"n": 2},
            "output": 3,
            "ex": None,
        },
        {
            "label": "three",
            "input": {"n": 3},
            "output": 4,
            "ex": None,
        },
        {
            "label": "ten",
            "input": {"n": 10},
            "output": 18,
            "ex": None,
        },
        {
            "label": "sixteen",
            "input": {"n": 16},
            "output": 31,
            "ex": None,
        },
        {
            "label": "hundred",
            "input": {"n": 100},
            "output": 217,
            "ex": None,
        },
        {
            "label": "1013",
            "input": {"n": 1013},
            "output": 1014,
            "ex": None,
        },
        {
            "label": "381024",
            "input": {"n": 381024},
            "output": 1307124,
            "ex": None,
        },
    ]
    for case in cases:
        try:
            output = sum_of_divisors(**case["input"])
            assert output == case["output"], "case '{}', output: exp {}, got {}".format(
                case["label"], case["output"], output
            )
        except Exception as e:
            assert type(e) == case["ex"], "case '{}', ex: exp {}, got {}".format(
                case["label"], case["ex"], type(e)
            )
