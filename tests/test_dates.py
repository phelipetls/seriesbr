import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from seriesbr.helpers.dates import parse_date


class TestDates(unittest.TestCase):

    def test_month_year_date(self):
        test = parse_date("08-2018", api="bcb")
        correct = "01/08/2018"
        self.assertEqual(test, correct)

    def test_complete_date(self):
        test = parse_date("01-12-2018", api="bcb")
        correct = "01/12/2018"
        self.assertEqual(test, correct)

    def test_year_date_start(self):
        test = parse_date("2018", api="bcb")
        correct = "01/01/2018"
        self.assertEqual(test, correct)

    def test_year_date_end(self):
        test = parse_date("2018", api="bcb", start=False)
        correct = "31/12/2018"
        self.assertEqual(test, correct)

    def test_date_locale_abbreviated_month(self):
        test = parse_date("oct2018", api="bcb")
        correct = "01/10/2018"
        self.assertEqual(test, correct)

    def test_date_locale_complete_month(self):
        test = parse_date("january2018", api="bcb")
        correct = "01/01/2018"
        self.assertEqual(test, correct)


if __name__ == "__main__":
    unittest.main()

# vi: nowrap
