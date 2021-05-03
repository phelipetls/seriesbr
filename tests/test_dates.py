from datetime import datetime
from seriesbr.helpers import dates


class TestDates:
    """Test date parser function"""

    def test_date_fully_specified(self):
        assert dates.parse_start_date("01-12-2018", api="bcb") == "01/12/2018"
        assert dates.parse_end_date("01-12-2018", api="bcb") == "01/12/2018"

    def test_date_month_and_year(self):
        assert dates.parse_start_date("08-2018", api="bcb") == "01/08/2018"

    def test_date_year_as_start_date(self):
        assert dates.parse_start_date("2018", api="bcb") == "01/01/2018"

    def test_date_year_as_end_date(self):
        assert dates.parse_end_date("2018", api="bcb") == "31/12/2018"

    def test_date_month_and_year_as_end(self):
        assert dates.parse_end_date("10/2018", api="bcb") == "31/10/2018"
        assert dates.parse_end_date("02/2018", api="bcb") == "28/02/2018"


def test_month_to_quarter():
    assert dates.month_to_quarter("2019-03-01", "%Y-%m-%d") == datetime(2019, 1, 1)
    assert dates.month_to_quarter("2019-06-01", "%Y-%m-%d") == datetime(2019, 2, 1)
    assert dates.month_to_quarter("2019-09-01", "%Y-%m-%d") == datetime(2019, 3, 1)
    assert dates.month_to_quarter("2019-12-01", "%Y-%m-%d") == datetime(2019, 4, 1)


# vi: nowrap
