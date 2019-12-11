import os
import sys
import json
import pandas
import unittest
from unittest.mock import patch


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from seriesbr import ipea

def mocked_ipea_search_only_filter(SERNOME="", **fields):
    filter_query = ipea.ipea_make_filter_query(SERNOME, fields)
    return filter_query


@patch('seriesbr.ipea.search', mocked_ipea_search_only_filter)
class TestIPEASearch(unittest.TestCase):

    def test_search_filters(self):
        self.assertEqual(ipea.search(SERNOME="Spread"), "&$filter=contains(SERNOME,'Spread')")
        self.assertEqual(ipea.search(SERNOME="Spread", TEMCODIGO=12), "&$filter=contains(SERNOME,'Spread') and TEMCODIGO eq 12")
        self.assertEqual(ipea.search(SERNOME="Spread", TEMCODIGO=12, FNTNOME="IBGE"), "&$filter=contains(SERNOME,'Spread') and TEMCODIGO eq 12 and contains(FNTNOME,'IBGE')")
        self.assertEqual(ipea.search(TEMCODIGO=12, FNTNOME="IBGE"), "&$filter=TEMCODIGO eq 12 and contains(FNTNOME,'IBGE')")
        self.assertEqual(ipea.search(TEMCODIGO=12, FNTNOME="IBGE", SERNUMERICA=1), "&$filter=TEMCODIGO eq 12 and contains(FNTNOME,'IBGE') and SERNUMERICA eq 1")
        self.assertEqual(ipea.search(SERNOME="Selic", TEMCODIGO=12, FNTNOME="IBGE", SERNUMERICA=1), "&$filter=contains(SERNOME,'Selic') and TEMCODIGO eq 12 and contains(FNTNOME,'IBGE') and SERNUMERICA eq 1")


if __name__ == "__main__":
    unittest.main()

# vi: nowrap
