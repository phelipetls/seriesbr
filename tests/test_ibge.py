import os
import sys
import unittest
import pandas
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from seriesbr import ibge


class IBGEtest(unittest.TestCase):

    def test_simple_get_only_with_code(self):
        self.assertIsInstance(ibge.get_series(1712), pandas.DataFrame)

    def test_get_with_classifications(self):
        self.assertIsInstance(ibge.get_series(1712, classification={226: [4844, 96608, 96609], 218: 4780}), pandas.DataFrame)

    def test_get_with_variables(self):
        self.assertIsInstance(ibge.get_series(1712, variables=[214, 1982]), pandas.DataFrame)
        self.assertIsInstance(ibge.get_series(1712, variables=214), pandas.DataFrame)

    def test_get_with_locations(self):
        self.assertIsInstance(ibge.get_series(1705, mesoregion=[3501, 3301], city=[5208707]), pandas.DataFrame)

    def test_get_with_periods_with_month(self):
        self.assertIsInstance(ibge.get_series(1705, start="201601", end="201701", mesoregion=[3501, 3301], city=[5208707]), pandas.DataFrame)

    def test_get_with_periods_anual(self):
        self.assertIsInstance(ibge.get_series(1732, start="2001", end="2006"), pandas.DataFrame)

    def test_get_with_wrong_date(self):
        self.assertIsInstance(ibge.get_series(1732, start="200101", end="200601"), pandas.DataFrame)

    def test_list_functions(self):
        self.assertIsInstance(ibge.list_aggregates("Emprego"), pandas.DataFrame)

    def test_list_variables(self):
        self.assertIsInstance(ibge.list_variables(1712), pandas.DataFrame)

    def test_list_states(self):
        self.assertIsInstance(ibge.list_states(), pandas.DataFrame)

    def test_list_macroregions(self):
        self.assertIsInstance(ibge.list_macroregions(), pandas.DataFrame)

    def test_list_microregions(self):
        self.assertIsInstance(ibge.list_microregions(), pandas.DataFrame)

    def test_list_cities(self):
        self.assertIsInstance(ibge.list_cities(), pandas.DataFrame)

    def test_list_mesoregions(self):
        self.assertIsInstance(ibge.list_mesoregions(), pandas.DataFrame)

    def test_build_classification_for_url(self):
        self.assertEqual(ibge.build_classification_query({26: [881, 9630], 25: [], 12: "all", "45": [236, 47]}), "classificacao=26[881,9630]|25[all]|12[all]|45[236,47]")

    def test_build_dates_for_url(self):
        today = datetime.today().strftime('%Y%m')
        self.assertEqual(ibge.build_dates_query(last_n=100), "/periodos/-100")
        self.assertEqual(ibge.build_dates_query(start=201802), f"/periodos/201802-{today}")
        self.assertEqual(ibge.build_dates_query(start=201804, end=201901), "/periodos/201804-201901")
        self.assertEqual(ibge.build_dates_query(end=2017), "/periodos/190001-2017")


if __name__ == "__main__":
    unittest.main()
