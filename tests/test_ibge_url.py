import sys
import unittest

from unittest.mock import patch
from mock_helpers import mocked_get_today_date
from seriesbr.helpers.api import (
    ibge_dates,
    ibge_classifications,
    ibge_locations,
    ibge_variables,
)


@patch("seriesbr.helpers.dates.get_today_date", mocked_get_today_date)
class TestIbgeDates(unittest.TestCase):
    def test_last_n(self):
        test = ibge_dates(last_n=5)
        expected = "/periodos/-5"
        self.assertEqual(test, expected)

    def test_start(self):
        test = ibge_dates(start="01/2017")
        expected = "/periodos/201701-201912"
        self.assertEqual(test, expected)

    def test_end(self):
        test = ibge_dates(end="07/2017")
        expected = "/periodos/190001-201707"
        self.assertEqual(test, expected)

    def test_start_and_end(self):
        test = ibge_dates(start="05-2015", end="07-2017")
        expected = "/periodos/201505-201707"
        self.assertEqual(test, expected)

    def test_start_and_end_yearly(self):
        test = ibge_dates(start="05-2015", end="07-2017", freq="anual")
        expected = "/periodos/2015-2017"
        self.assertEqual(test, expected)

    def test_start_and_end_quarterly(self):
        test = ibge_dates(start="05-2015", end="07-2017", freq="trimestral")
        expected = "/periodos/201502-201703"
        self.assertEqual(test, expected)


class TestIbgeVariables(unittest.TestCase):
    def test_empty(self):
        test = ibge_variables()
        expected = "/variaveis"
        self.assertEqual(test, expected)

    def test_int(self):
        test = ibge_variables(100)
        expected = "/variaveis/100"
        self.assertEqual(test, expected)

    def test_str(self):
        test = ibge_variables("100")
        expected = "/variaveis/100"
        self.assertEqual(test, expected)

    def test_list(self):
        test = ibge_variables([1, 2, 3])
        expected = "/variaveis/1|2|3"
        self.assertEqual(test, expected)


class TestIbgeLocations(unittest.TestCase):
    def test_empty(self):
        test = ibge_locations()
        expected = "&localidades=BR"
        self.assertEqual(test, expected)

    def test_dict_with_nones(self):
        test = ibge_locations(cities=None, municipalities=None)
        expected = "&localidades=BR"
        self.assertEqual(test, expected)

    def test_brazil_non_false(self):
        test = ibge_locations(brazil="yes")
        expected = "&localidades=BR"
        self.assertEqual(test, expected)

    def test_bool(self):
        test = ibge_locations(states=True)
        expected = "&localidades=N3"
        self.assertEqual(test, expected)

    def test_truthy(self):
        test = ibge_locations(states="all")
        expected = "&localidades=N3"
        self.assertEqual(test, expected)

    def test_int(self):
        test = ibge_locations(states=2)
        expected = "&localidades=N3[2]"
        self.assertEqual(test, expected)

    def test_list(self):
        test = ibge_locations(states=[2, 3, 4])
        expected = "&localidades=N3[2,3,4]"
        self.assertEqual(test, expected)

    def test_multiple_args(self):
        test = ibge_locations(states=[2, 3, 4], municipalities=[1, 2])
        expected = "&localidades=N3[2,3,4]|N6[1,2]"
        self.assertEqual(test, expected)

    @unittest.skipIf(sys.version_info.minor < 7, "Unpredictable order of dictionaries")
    def test_multiple_args_mixed_types(self):
        test = ibge_locations(states=True, mesoregions=4, municipalities=[1, 2])
        expected = "&localidades=N3|N7[4]|N6[1,2]"
        self.assertEqual(test, expected)


class TestIbgeClassifications(unittest.TestCase):
    def test_none(self):
        test = ibge_classifications()
        expected = ""
        self.assertEqual(test, expected)

    def test_str(self):
        test = ibge_classifications("3")
        expected = "classificacao=3[all]"
        self.assertEqual(test, expected)

    def test_int(self):
        test = ibge_classifications(3)
        expected = "classificacao=3[all]"
        self.assertEqual(test, expected)

    def test_list(self):
        test = ibge_classifications([1, 2])
        expected = "classificacao=1[all]|2[all]"
        self.assertEqual(test, expected)

    def test_dict(self):
        test = ibge_classifications({1: [2, 3]})
        expected = "classificacao=1[2,3]"
        self.assertEqual(test, expected)

    def test_dict_multiple_keys(self):
        test = ibge_classifications({1: [2, 3], 4: [5, 6]})
        expected = "classificacao=1[2,3]|4[5,6]"
        self.assertEqual(test, expected)

    def test_empty_dict(self):
        test = ibge_classifications({1: []})
        expected = "classificacao=1[all]"
        self.assertEqual(test, expected)


if __name__ == "__main__":
    unittest.main(failfast=True)

# vi: nowrap
