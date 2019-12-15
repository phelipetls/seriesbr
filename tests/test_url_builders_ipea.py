import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import seriesbr.helpers.url as url


class TestUrlBuildersIPEA(unittest.TestCase):

    def test_select_query_default_queries(self):
        correct = "?$select=SERCODIGO,SERNOME,PERNOME,UNINOME"
        test = url.ipea_make_select_query(["SERCODIGO", "SERNOME"])
        self.assertEqual(test, correct)

    def test_select_query_additional_queries(self):
        correct = "?$select=SERCODIGO,SERNOME,PERNOME,UNINOME,FNTNOME"
        test = url.ipea_make_select_query(["FNTNOME"])
        self.assertEqual(test, correct)

    def test_numeric_filter_query_no_name(self):
        correct = "&$filter=SERNUMERICA eq 1"
        test = url.ipea_make_filter_query(names=None, fields={'SERNUMERICA': 1})
        self.assertEqual(test, correct)

    def test_string_filter_query_no_name(self):
        correct = "&$filter=contains(FNTNOME,'BCB')"
        test = url.ipea_make_filter_query(names=None, fields={'FNTNOME': 'BCB'})
        self.assertEqual(test, correct)

    def test_string_and_numeric_filters_query_with_name(self):
        correct = "&$filter=contains(SERNOME,'Spread') and contains(FNTNOME,'BCB') and TEMCODIGO eq 1"
        test = url.ipea_make_filter_query(names="Spread", fields={'FNTNOME': 'BCB', 'TEMCODIGO': 1})
        self.assertEqual(test, correct)

    def test_raises_if_invalid_field(self):
        with self.assertRaises(ValueError):
            url.ipea_make_filter_query("", {"INVALID_FILTER": "INVALID"})


if __name__ == "__main__":
    unittest.main()

# vi: nowrap
