import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from seriesbr.helpers.dates import parse_date  # noqa: E402


class TestDates(unittest.TestCase):
    """Test date parser function"""

    def test_date_with_month_and_year(self):
        test = parse_date("08-2018", api="bcb")
        expected = "01/08/2018"
        self.assertEqual(test, expected)

    def test_date_full(self):
        test = parse_date("01-12-2018", api="bcb")
        expected = "01/12/2018"
        self.assertEqual(test, expected)

    def test_date_with_year_only_as_start_date(self):
        test = parse_date("2018", api="bcb")
        expected = "01/01/2018"
        self.assertEqual(test, expected)

    def test_date_with_year_only_as_end_date(self):
        test = parse_date("2018", api="bcb", start=False)
        expected = "31/12/2018"
        self.assertEqual(test, expected)

    def test_date_abbreviated_month(self):
        test = parse_date("oct2018", api="bcb")
        expected = "01/10/2018"
        self.assertEqual(test, expected)

    def test_date_complete_month(self):
        test = parse_date("january2018", api="bcb")
        expected = "01/01/2018"
        self.assertEqual(test, expected)


if __name__ == "__main__":
    unittest.main()

# vi: nowrap
