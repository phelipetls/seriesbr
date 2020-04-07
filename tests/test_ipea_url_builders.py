import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import seriesbr.helpers.url as url  # noqa: E402


class TestUrlBuildersIPEA(unittest.TestCase):
    """Test function that help build a IBGE API call"""

    def test_select_query_default_queries(self):
        expected = "?$select=SERCODIGO,SERNOME,PERNOME,UNINOME"
        test = url.ipea_select(["SERCODIGO", "SERNOME"])
        self.assertEqual(test, expected)

    def test_select_query_additional_queries(self):
        expected = "?$select=SERCODIGO,SERNOME,PERNOME,UNINOME,FNTNOME"
        test = url.ipea_select(["FNTNOME"])
        self.assertEqual(test, expected)

    def test_filter_query_numeric_with_no_name(self):
        expected = "&$filter=SERNUMERICA eq 1"
        test = url.ipea_filter(names=None, metadatas={"SERNUMERICA": 1})
        self.assertEqual(test, expected)

    def test_filter_query_string_no_name(self):
        expected = "&$filter=contains(FNTNOME,'BCB')"
        test = url.ipea_filter(names=None, metadatas={"FNTNOME": "BCB"})
        self.assertEqual(test, expected)

    def test_filters_query_string_and_numeric__with_name(self):
        expected = "&$filter=contains(SERNOME,'Spread') and contains(FNTNOME,'BCB') and TEMCODIGO eq 1"
        test = url.ipea_filter(
            names="Spread", metadatas={"FNTNOME": "BCB", "TEMCODIGO": 1}
        )
        self.assertEqual(test, expected)

    def test_filters_query_string_and_numeric_with_multiple_names(self):
        expected = "&$filter=(contains(SERNOME,'Spread') and contains(SERNOME,'Taxa'))"
        test = url.ipea_filter(names=["Spread", "Taxa"])
        self.assertEqual(test, expected)

    def test_raises_if_invalid_field(self):
        with self.assertRaises(ValueError):
            url.ipea_filter("", {"INVALID_FILTER": "INVALID"})

    def test_dates_query_start_and_end(self):
        expected = "&$filter=VALDATA ge 2019-01-01T00:00:00-00:00 and VALDATA le 2019-01-01T00:00:00-00:00"
        test = url.ipea_date(
            start="2019-01-01T00:00:00-00:00", end="2019-01-01T00:00:00-00:00"
        )
        self.assertEqual(test, expected)

    def test_dates_query_start(self):
        expected = "&$filter=VALDATA ge 2019-01-01T00:00:00-00:00"
        test = url.ipea_date(start="2019-01-01T00:00:00-00:00")
        self.assertEqual(test, expected)

    def test_dates_query_end(self):
        expected = "&$filter=VALDATA le 2019-01-01T00:00:00-00:00"
        test = url.ipea_date(end="2019-01-01T00:00:00-00:00")
        self.assertEqual(test, expected)


if __name__ == "__main__":
    unittest.main()

# vi: nowrap
