import datetime
import json
from unittest.mock import patch, mock_open
import pytest

from aoc_lib.combinatorics import *


def test_binom():
    cases = [
        {
            "label": "simple",
            "input": {"n": 5, "k": 3},
            "output": 10,
            "ex": None,
        },
        {
            "label": "id",
            "input": {"n": 5, "k": 5},
            "output": 1,
            "ex": None,
        },
        {
            "label": "one element",
            "input": {"n": 5, "k": 1},
            "output": 5,
            "ex": None,
        },
        {
            "label": "big",
            "input": {"n": 5000, "k": 424},
            "output": 58785925141557944909305041943834971831583181859069692508231715611491119626582200383280457153390910595512259899122882520765087895098175664033398989169316774060627105597210636603621323545812546402581476330186674424396031129850763266200892496323203376075081410013237246600753328169640962517981588664980395966980925791409302226107670765554196760123665806402984312126493260045593122474676646720855248311086632360206126299556042710056444382994389655069027051741582803582632709133216079376085048223012538051368603350307155359664134736512664372570239582512041499394781396942840361112917432663817107692940406224434354507691553099812930000,
            "ex": None,
        },
    ]
    for case in cases:
        try:
            output = binom(**case["input"])
            assert output == case["output"], "case '{}', output: exp {}, got {}".format(
                case["label"], case["output"], output
            )
        except Exception as e:
            assert type(e) == case["ex"], "case '{}', ex: exp {}, got {}".format(
                case["label"], case["ex"], type(e)
            )


def test_buckles():
    cases = [
        {
            "label": "simple",
            "input": {"elements": 3, "choice_length": 2, "comb_index": 0},
            "output": [0, 1],
            "ex": None,
        },
        {
            "label": "simple2",
            "input": {"elements": 7, "choice_length": 3, "comb_index": 4},
            "output": [0, 1, 6],
            "ex": None,
        },
        {
            "label": "zero one",
            "input": {"elements": 7, "choice_length": 1, "comb_index": 0},
            "output": [0],
            "ex": None,
        },
    ]
    for case in cases:
        try:
            output = buckles(**case["input"])
            assert output == case["output"], "case '{}', output: exp {}, got {}".format(
                case["label"], case["output"], output
            )
        except Exception as e:
            assert type(e) == case["ex"], "case '{}', ex: exp {}, got {}".format(
                case["label"], case["ex"], type(e)
            )
