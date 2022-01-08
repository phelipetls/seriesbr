import pytest
from datetime import datetime
from seriesbr.utils import dates


def test_month_to_quarter():
    assert dates.month_to_quarter("2019-03-01", "%Y-%m-%d") == datetime(2019, 1, 1)
    assert dates.month_to_quarter("2019-06-01", "%Y-%m-%d") == datetime(2019, 2, 1)
    assert dates.month_to_quarter("2019-09-01", "%Y-%m-%d") == datetime(2019, 3, 1)
    assert dates.month_to_quarter("2019-12-01", "%Y-%m-%d") == datetime(2019, 4, 1)
