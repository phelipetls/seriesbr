import os
import sys
import unittest
from unittest.mock import patch


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from seriesbr import ipea


def mocked_ipea_search_only_filter(SERNOME="", **fields):
    filter_query = ipea.ipea_make_filter_query(SERNOME, fields)
    return filter_query


@patch('seriesbr.ipea.search', mocked_ipea_search_only_filter)
class TestIPEASearch(unittest.TestCase):

    def test_simple_search_filter(self):
        test = ipea.search(SERNOME="Spread")
        correct = "&$filter=contains(SERNOME,'Spread')"
        self.assertEqual(test, correct)

    def test_search_alpha_and_numeric_filter(self):
        test = ipea.search(SERNOME="Spread", TEMCODIGO=12)
        correct = "&$filter=contains(SERNOME,'Spread') and TEMCODIGO eq 12"
        self.assertEqual(test, correct)

    def test_search_three_filters_all_mixed(self):
        test = ipea.search(SERNOME="Spread", TEMCODIGO=12, FNTNOME="IBGE")
        correct = "&$filter=contains(SERNOME,'Spread') and TEMCODIGO eq 12 and contains(FNTNOME,'IBGE')"
        self.assertEqual(test, correct)

    def test_search_without_name(self):
        test = ipea.search(TEMCODIGO=12, FNTNOME="IBGE")
        correct = "&$filter=TEMCODIGO eq 12 and contains(FNTNOME,'IBGE')"
        self.assertEqual(test, correct)

    def test_search_without_name_mixed_types(self):
        test = ipea.search(TEMCODIGO=12, FNTNOME="IBGE", SERNUMERICA=1)
        correct = "&$filter=TEMCODIGO eq 12 and contains(FNTNOME,'IBGE') and SERNUMERICA eq 1"
        self.assertEqual(test, correct)

    def test_search_multiple_types_four_filters(self):
        test = ipea.search(SERNOME="Selic", TEMCODIGO=12, FNTNOME="IBGE", SERNUMERICA=1)
        correct = "&$filter=contains(SERNOME,'Selic') and TEMCODIGO eq 12 and contains(FNTNOME,'IBGE') and SERNUMERICA eq 1"
        self.assertEqual(test, correct)

    def test_search_multiple_types_including_country_code(self):
        test = ipea.search(SERNOME="Selic", TEMCODIGO=12, FNTNOME="IBGE", SERNUMERICA=1, PAICODIGO="SAU")
        correct = "&$filter=contains(SERNOME,'Selic') and TEMCODIGO eq 12 and contains(FNTNOME,'IBGE') and SERNUMERICA eq 1 and PAICODIGO eq 'SAU'"
        self.assertEqual(test, correct)

    def test_search_list_values_name_and_equal_operator_int(self):
        test = ipea.search(SERNOME="Selic", TEMCODIGO=[12, 14])
        correct = "&$filter=contains(SERNOME,'Selic') and (TEMCODIGO eq 12 or TEMCODIGO eq 14)"
        self.assertEqual(test, correct)

    def test_search_list_values_name_and_equal_operator_string(self):
        test = ipea.search(SERNOME="Selic", PAICODIGO=["USA", "BRA"])
        correct = "&$filter=contains(SERNOME,'Selic') and (PAICODIGO eq 'USA' or PAICODIGO eq 'BRA')"
        self.assertEqual(test, correct)

    def test_search_list_values_in_name(self):
        test = ipea.search(SERNOME=["Selic", "Spread"], PAICODIGO=["USA", "BRA"], TEMCODIGO=[12, 13])
        correct = "&$filter=(contains(SERNOME,'Selic') or contains(SERNOME,'Spread')) and (PAICODIGO eq 'USA' or PAICODIGO eq 'BRA') and (TEMCODIGO eq 12 or TEMCODIGO eq 13)"
        self.assertEqual(test, correct)

    def test_search_list_values_without_names(self):
        test = ipea.search(PAICODIGO=["USA", "BRA"], UNINOME=["%", "(% a.a.)"])
        correct = "&$filter=(PAICODIGO eq 'USA' or PAICODIGO eq 'BRA') and (contains(UNINOME,'%') or contains(UNINOME,'(% a.a.)'))"
        self.assertEqual(test, correct)

    def test_search_list_values_only_contains(self):
        test = ipea.search(FNTNOME=["IBGE", "CAGED"], UNINOME=["%", "(% a.a.)"])
        correct = "&$filter=(contains(FNTNOME,'IBGE') or contains(FNTNOME,'CAGED')) and (contains(UNINOME,'%') or contains(UNINOME,'(% a.a.)'))"
        self.assertEqual(test, correct)


if __name__ == "__main__":
    unittest.main()

# vi: nowrap
