import pytest
from datetime import datetime
from seriesbr.helpers import dates


class TestDates:
    """Test date parser function"""

    @pytest.mark.parametrize("api,expected", [
        ("bcb", "01/12/2018"),
        ("ipea", "2018-12-01T00:00:00Z"),
        ("ibge", "201812")
    ])
    def test_full_date_as_start_date(self, api, expected):
        assert dates.parse_start_date("01-12-2018", api=api) == expected

    @pytest.mark.parametrize("api,expected", [
        ("bcb", "01/12/2018"),
        ("ipea", "2018-12-01T00:00:00Z"),
        ("ibge", "201812")
    ])
    def test_full_date_as_end_date(self, api, expected):
        assert dates.parse_end_date("01-12-2018", api=api) == expected

    @pytest.mark.parametrize("api,expected", [
        ("bcb", "01/12/2018"),
        ("ipea", "2018-12-01T00:00:00Z"),
        ("ibge", "201812")
    ])
    def test_date_month_and_year(self, api, expected):
        assert dates.parse_start_date("12-2018", api=api) == expected

    @pytest.mark.parametrize("api,expected", [
        ("bcb", "31/12/2018"),
        ("ipea", "2018-12-31T00:00:00Z"),
        ("ibge", "201812")
    ])
    def test_date_month_and_year_as_end(self, api, expected):
        assert dates.parse_end_date("12/2018", api=api) == expected

    @pytest.mark.parametrize("api,expected", [
        ("bcb", "01/01/2018"),
        ("ipea", "2018-01-01T00:00:00Z"),
        ("ibge", "201801")
    ])
    def test_date_year_as_start_date(self, api, expected):
        assert dates.parse_start_date("2018", api=api) == expected

    @pytest.mark.parametrize("api,expected", [
        ("bcb", "31/12/2018"),
        ("ipea", "2018-12-31T00:00:00Z"),
        ("ibge", "201812")
    ])
    def test_date_year_as_end_date(self, api, expected):
        assert dates.parse_end_date("2018", api=api) == expected


def test_month_to_quarter():
    assert dates.month_to_quarter("2019-03-01", "%Y-%m-%d") == datetime(2019, 1, 1)
    assert dates.month_to_quarter("2019-06-01", "%Y-%m-%d") == datetime(2019, 2, 1)
    assert dates.month_to_quarter("2019-09-01", "%Y-%m-%d") == datetime(2019, 3, 1)
    assert dates.month_to_quarter("2019-12-01", "%Y-%m-%d") == datetime(2019, 4, 1)


# vi: nowrap
