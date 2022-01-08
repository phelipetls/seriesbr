import pytest
from datetime import datetime
from seriesbr.utils import dates


def test_month_to_quarter():
    assert dates.month_to_quarter(datetime(2019, 3, 1)) == datetime(2019, 1, 1)
    assert dates.month_to_quarter(datetime(2019, 6, 1)) == datetime(2019, 2, 1)
    assert dates.month_to_quarter(datetime(2019, 9, 1)) == datetime(2019, 3, 1)
    assert dates.month_to_quarter(datetime(2019, 12, 1)) == datetime(2019, 4, 1)
