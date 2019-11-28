import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from seriesbr.helpers.dates import parse_date


class TestDates(unittest.TestCase):

    # this is done in cade that if start = "2017" and end = "2017",
    # the dates will cover the whole year ("01/01/2017"--"31/12/2017")
    # but, a day is specified by the user, end date should respect that.
    # same thing applys to a month.

    def test_start_dates_bcb(self):
        self.assertEqual(parse_date("2017", "bcb"), "01/01/2017")
        self.assertEqual(parse_date("01/01/2017", "bcb"), "01/01/2017")
        self.assertEqual(parse_date("01-01-2017", "bcb"), "01/01/2017")
        self.assertEqual(parse_date("01/2017", "bcb"), "01/01/2017")
        self.assertEqual(parse_date("01-2017", "bcb"), "01/01/2017")

    def test_end_dates_ipea(self):
        self.assertEqual(parse_date("2017", "bcb", start=False), "31/12/2017")
        self.assertEqual(parse_date("06/01/2017", "bcb", start=False), "06/01/2017")
        self.assertEqual(parse_date("06-01-2017", "bcb", start=False), "06/01/2017")
        self.assertEqual(parse_date("08/2017", "bcb", start=False), "31/08/2017")
        self.assertEqual(parse_date("08-2017", "bcb", start=False), "31/08/2017")


if __name__ == "__main__":
    unittest.main()
