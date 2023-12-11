import datetime
import json
from unittest.mock import patch, mock_open
import pytest

from aoc_lib.interval import Interval

def test_interval_contains():
    cases = [
        {
            "label": "middle",
            "init": {"start":0, "end":10},
            "input": {"other":Interval(1,6)},
            "output": True,
            "ex": None,
        },
        {
            "label": "start edge",
            "init": {"start":0, "end":10},
            "input": {"other":Interval(0,6)},
            "output": True,
            "ex": None,
        },
        {
            "label": "end edge",
            "init": {"start":0, "end":10},
            "input": {"other":Interval(1,10)},
            "output": True,
            "ex": None,
        },
        {
            "label": "identity",
            "init": {"start":0, "end":10},
            "input": {"other":Interval(0,10)},
            "output": True,
            "ex": None,
        },
        {
            "label": "outward contain",
            "init": {"start":0, "end":10},
            "input": {"other":Interval(-1,12)},
            "output": False,
            "ex": None,
        },
        {
            "label": "outward contain, same end",
            "init": {"start":0, "end":10},
            "input": {"other":Interval(-1,10)},
            "output": False,
            "ex": None,
        },
        {
            "label": "outward contain, same start",
            "init": {"start":0, "end":10},
            "input": {"other":Interval(0,12)},
            "output": False,
            "ex": None,
        },
        {
            "label": "intersection",
            "init": {"start":0, "end":10},
            "input": {"other":Interval(8,12)},
            "output": False,
            "ex": None,
        },
        {
            "label": "disjoined",
            "init": {"start":0, "end":10},
            "input": {"other":Interval(12,16)},
            "output": False,
            "ex": None,
        },
    ]
    for case in cases:
        try:
            obj = Interval(**case["init"])
            output = obj.contains(**case["input"])
            assert output == case["output"], "case '{}', output: exp {}, got {}".format(
                case["label"], case["output"], output
            )
        except Exception as e:
            assert type(e) == case["ex"], "case '{}', ex: exp {}, got {}".format(
                case["label"], case["ex"], type(e)
            )


def test_interval_overlap_other():
    cases = [
        {
            "label": "middle",
            "init": {"start":0, "end":10},
            "input": {"other":Interval(1,6)},
            "output": True,
            "ex": None,
        },
        {
            "label": "start edge",
            "init": {"start":0, "end":10},
            "input": {"other":Interval(0,6)},
            "output": True,
            "ex": None,
        },
        {
            "label": "end edge",
            "init": {"start":0, "end":10},
            "input": {"other":Interval(1,10)},
            "output": True,
            "ex": None,
        },
        {
            "label": "identity",
            "init": {"start":0, "end":10},
            "input": {"other":Interval(0,10)},
            "output": True,
            "ex": None,
        },
        {
            "label": "outward contain",
            "init": {"start":0, "end":10},
            "input": {"other":Interval(-1,12)},
            "output": True,
            "ex": None,
        },
        {
            "label": "outward contain, same end",
            "init": {"start":0, "end":10},
            "input": {"other":Interval(-1,10)},
            "output": True,
            "ex": None,
        },
        {
            "label": "outward contain, same start",
            "init": {"start":0, "end":10},
            "input": {"other":Interval(0,12)},
            "output": True,
            "ex": None,
        },
        {
            "label": "intersection",
            "init": {"start":0, "end":10},
            "input": {"other":Interval(8,12)},
            "output": True,
            "ex": None,
        },
        {
            "label": "disjoined",
            "init": {"start":0, "end":10},
            "input": {"other":Interval(12,16)},
            "output": False,
            "ex": None,
        },
    ]
    for case in cases:
        try:
            obj = Interval(**case["init"])
            output = obj.overlap_other(**case["input"])
            assert output == case["output"], "case '{}', output: exp {}, got {}".format(
                case["label"], case["output"], output
            )
        except Exception as e:
            assert type(e) == case["ex"], "case '{}', ex: exp {}, got {}".format(
                case["label"], case["ex"], type(e)
            )


def test_interval_overlap():
    cases = [
        {
            "label": "middle",
            "input": {"a":Interval(0,10), "b":Interval(1,6)},
            "output": True,
            "ex": None,
        },
        {
            "label": "start edge",
            "input": {"a":Interval(0,10), "b":Interval(0,6)},
            "output": True,
            "ex": None,
        },
        {
            "label": "end edge",
            "input": {"a":Interval(0,10), "b":Interval(1,10)},
            "output": True,
            "ex": None,
        },
        {
            "label": "identity",
            "input": {"a":Interval(0,10), "b":Interval(0,10)},
            "output": True,
            "ex": None,
        },
        {
            "label": "outward contain",
            "input": {"a":Interval(0,10), "b":Interval(-1,12)},
            "output": True,
            "ex": None,
        },
        {
            "label": "outward contain, same end",
            "input": {"a":Interval(0,10), "b":Interval(-1,10)},
            "output": True,
            "ex": None,
        },
        {
            "label": "outward contain, same start",
            "input": {"a":Interval(0,10), "b":Interval(0,12)},
            "output": True,
            "ex": None,
        },
        {
            "label": "intersection",
            "input": {"a":Interval(0,10), "b":Interval(8,12)},
            "output": True,
            "ex": None,
        },
        {
            "label": "disjoined",
            "input": {"a":Interval(0,10), "b":Interval(12,16)},
            "output": False,
            "ex": None,
        },
    ]
    for case in cases:
        try:
            output = Interval.overlap(**case["input"])
            assert output == case["output"], "case '{}', output: exp {}, got {}".format(
                case["label"], case["output"], output
            )
        except Exception as e:
            assert type(e) == case["ex"], "case '{}', ex: exp {}, got {}".format(
                case["label"], case["ex"], type(e)
            )

def test_least_common_intervals():
    cases = [
        {
            "label": "middle",
            "input": {"list_a":[Interval(0,10)], "list_b":[Interval(0,0), Interval(1,6), Interval(7,10)]},
            "output": [Interval(0,0),Interval(1,6), Interval(7,10)],
            "ex": None,
        },
        {
            "label": "start edge",
            "input": {"list_a":[Interval(0,10)], "list_b":[Interval(0,6), Interval(7,10)]},
            "output": [Interval(0,6), Interval(7,10)],
            "ex": None,
        },
        {
            "label": "end edge",
            "input": {"list_a":[Interval(0,10)], "list_b":[Interval(0,2),Interval(3,10)]},
            "output": [Interval(0,2), Interval(3,10)],
            "ex": None,
        },
        {
            "label": "identity",
            "input": {"list_a":[Interval(0,10)], "list_b":[Interval(0,10)]},
            "output": [Interval(0,10)],
            "ex": None,
        },
        {
            "label": "intersection",
            "input": {"list_a":[Interval(0,10), Interval(11,16)], "list_b":[Interval(0,7), Interval(8,12), Interval(13,16)]},
            "output": [Interval(0,7), Interval(8,10), Interval(11,12),Interval(13,16)],
            "ex": None,
        },
    ]
    for case in cases:
        try:
            output = Interval.least_common_intervals(**case["input"])
            assert output == case["output"], "case '{}', output: exp {}, got {}".format(
                case["label"], case["output"], output
            )
        except Exception as e:
            assert type(e) == case["ex"], "case '{}', ex: exp {}, got {}".format(
                case["label"], case["ex"], type(e)
            )


def test_label_mask():
    cases = [
        {
            "label": "simple",
            "input": {"list_a":[Interval(0,0), Interval(1,6), Interval(7,10)], "mask":[Interval(1,6,'good')]},
            "output": [Interval(0,0),Interval(1,6,'good'), Interval(7,10)],
            "ex": None,
        },
        {
            "label": "big mask",
            "input": {"list_a":[Interval(0,7), Interval(8,10), Interval(11,12),Interval(13,16)], "mask":[Interval(0,12, 'good'),]},
            "output": [Interval(0,7,'good'), Interval(8,10,'good'), Interval(11,12,'good'),Interval(13,16,'bad')],
            "ex": None,
        },
        {
            "label": "holed mask",
            "input": {"list_a":[Interval(0,7), Interval(8,10), Interval(11,12),Interval(13,16)], "mask":[Interval(0,7, 'good'), Interval(11,12,'good')]},
            "output": [Interval(0,7,'good'), Interval(8,10,'bad'), Interval(11,12,'good'),Interval(13,16,'bad')],
            "ex": None,
        },
    ]
    for case in cases:
        try:
            output = Interval.label_mask(**case["input"])
            assert case["input"]["list_a"] == case["output"], "case '{}', output: exp {}, got {}".format(
                case["label"], case["output"], output
            )
        except Exception as e:
            assert type(e) == case["ex"], "case '{}', ex: exp {}, got {}".format(
                case["label"], case["ex"], type(e)
            )


def test_fill_holes():
    cases = [
        {
            "label": "simple",
            "input": {"list_a":[Interval(0,0), Interval(7,10)], "label":'good'},
            "output": [Interval(0,0),Interval(1,6,'good'), Interval(7,10)],
            "ex": None,
        },
        {
            "label": "two holes",
            "input": {"list_a":[Interval(0,7), Interval(11,12),Interval(15,16)], "label":'good'},
            "output": [Interval(0,7), Interval(8,10,'good'), Interval(11,12),Interval(13,14,'good'), Interval(15,16)],
            "ex": None,
        },
    ]
    for case in cases:
        try:
            output = Interval.fill_holes(**case["input"])
            assert output == case["output"], "case '{}', output: exp {}, got {}".format(
                case["label"], case["output"], output
            )
        except Exception as e:
            assert type(e) == case["ex"], "case '{}', ex: exp {}, got {}".format(
                case["label"], case["ex"], type(e)
            )


def test_normalize():
    cases = [
        {
            "label": "simple",
            "input": {"list_a":[Interval(7,10)], "label":'good'},
            "output": [Interval(0,6,'good'),Interval(7,10), Interval(11,float('inf'),'good')],
            "ex": None,
        },
        {
            "label": "two holes",
            "input": {"list_a":[Interval(7,12),Interval(15,16)], "label":'good'},
            "output": [Interval(0,6,'good'), Interval(7,12), Interval(15,16), Interval(17,float('inf'),'good')],
            "ex": None,
        },
    ]
    for case in cases:
        try:
            output = Interval.normalize(**case["input"])
            assert output == case["output"], "case '{}', output: exp {}, got {}".format(
                case["label"], case["output"], output
            )
        except Exception as e:
            assert type(e) == case["ex"], "case '{}', ex: exp {}, got {}".format(
                case["label"], case["ex"], type(e)
            )

def test_find_intervals():
    cases = [
        {
            "label": "simple",
            "input": {"list_a":[Interval(0,7,'good'), Interval(8,10,'bad'), Interval(11,12,'good'),Interval(13,16,'bad')], "b":Interval(6,12)},
            "output": [Interval(8,10,'bad'),Interval(11,12,'good')],
            "ex": None,
        },
    ]
    for case in cases:
        try:
            output = Interval.find_intervals(**case["input"])
            assert output == case["output"], "case '{}', output: exp {}, got {}".format(
                case["label"], case["output"], output
            )
        except Exception as e:
            assert type(e) == case["ex"], "case '{}', ex: exp {}, got {}".format(
                case["label"], case["ex"], type(e)
            )
