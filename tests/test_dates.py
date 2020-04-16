import unittest

from datetime import datetime
from seriesbr.helpers import dates


class TestDates(unittest.TestCase):
    """Test date parser function"""

    def test_date_with_month_and_year(self):
        test = dates.parse_date("08-2018", api="bcb")
        expected = "01/08/2018"
        self.assertEqual(test, expected)

    def test_date_full(self):
        test = dates.parse_date("01-12-2018", api="bcb")
        expected = "01/12/2018"
        self.assertEqual(test, expected)

    def test_date_with_year_only_as_start_date(self):
        test = dates.parse_date("2018", api="bcb")
        expected = "01/01/2018"
        self.assertEqual(test, expected)

    def test_date_with_year_only_as_end_date(self):
        test = dates.parse_date("2018", api="bcb", start=False)
        expected = "31/12/2018"
        self.assertEqual(test, expected)

    def test_date_abbreviated_month(self):
        test = dates.parse_date("oct2018", api="bcb")
        expected = "01/10/2018"
        self.assertEqual(test, expected)

    def test_date_complete_month(self):
        test = dates.parse_date("january2018", api="bcb")
        expected = "01/01/2018"
        self.assertEqual(test, expected)

    quarters = {
        "2019-03-01": datetime(2019, 1, 1),
        "2019-06-01": datetime(2019, 2, 1),
        "2019-09-01": datetime(2019, 3, 1),
        "2019-12-01": datetime(2019, 4, 1),
    }

    def test_month_to_quarter(self):
        """Test if month is converted to the proper quarter"""

        for quarter, expected in self.quarters.items():
            with self.subTest(quarter):
                test = dates.month_to_quarter(quarter, "%Y-%m-%d")
                self.assertEqual(test, expected)


if __name__ == "__main__":
    unittest.main()

# vi: nowrap
