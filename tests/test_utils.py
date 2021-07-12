import pytest
import pandas as pd

from seriesbr.utils import misc


def test_cat():
    assert misc.cat(2, ",") == 2
    assert misc.cat("123", ",") == "123"
    assert misc.cat([1, 2, 3, 4], ",") == "1,2,3,4"
    assert misc.cat((4, 5), ",") == "4,5"


def test_is_isterable():
    assert misc.is_iterable([1])
    assert misc.is_iterable((1,))
    assert misc.is_iterable({1: 1})
    assert not misc.is_iterable(1)
    assert not misc.is_iterable("1")


def test_parse_arguments():
    assert misc.parse_arguments({"A": 1, "B": 2}, 100) == {"A": 1, "B": 2, 100: 100}


def test_parse_arguments_without_dictionary():
    assert misc.parse_arguments(11) == {11: 11}
