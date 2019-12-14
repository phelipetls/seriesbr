import os
import sys
import json
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from seriesbr import ibge


def get_sample_json(resource):
    json_path = Path(__file__).resolve().parent / "sample_jsons"
    if resource == "ibge_variables":
        json_path /= "ibge_variables"
    if resource == "ibge_metadata":
        json_path /= "ibge_metadata"
    if resource == "regioes":
        json_path /= "ibge_regioes"
    if resource == "mesorregioes":
        json_path /= "ibge_mesorregioes"
    if resource == "microrregioes":
        json_path /= "ibge_microrregioes"
    if resource == "estados":
        json_path /= "ibge_estados"
    if resource == "municipios":
        json_path /= "ibge_municipios"
    with json_path.open() as json_file:
        return json.load(json_file)


class TestListMetadataFunctions(unittest.TestCase):

    @patch('seriesbr.ibge.get_json')
    def test_ibge_list_variables(self, mocked_get_json):
        mocked_get_json.return_value = get_sample_json("ibge_variables")
        self.assertFalse(ibge.list_variables(1419).empty)

    @patch('seriesbr.ibge.get_json')
    def test_ibge_list_locations(self, mocked_get_json):
        mocked_get_json.return_value = get_sample_json("ibge_metadata")
        self.assertFalse(ibge.list_locations(1419).empty)

    @patch('seriesbr.ibge.get_json')
    def test_ibge_list_periods(self, mocked_get_json):
        mocked_get_json.return_value = get_sample_json("ibge_metadata")
        self.assertFalse(ibge.list_periods(1419).empty)

    @patch('seriesbr.ibge.get_json')
    def test_ibge_list_classifications(self, mocked_get_json):
        mocked_get_json.return_value = get_sample_json("ibge_metadata")
        self.assertFalse(ibge.list_classifications(1419).empty)


class TestListRegionsFunctions(unittest.TestCase):

    @patch('seriesbr.helpers.lists.get_json')
    def test_list_macroregions(self, mocked_get_json):
        mocked_get_json.return_value = get_sample_json("regioes")
        self.assertFalse(ibge.list_macroregions().empty)

    @patch('seriesbr.helpers.lists.get_json')
    def test_list_microregions(self, mocked_get_json):
        mocked_get_json.return_value = get_sample_json("microrregioes")
        self.assertFalse(ibge.list_microregions().empty)

    @patch('seriesbr.helpers.lists.get_json')
    def test_list_mesoregions(self, mocked_get_json):
        mocked_get_json.return_value = get_sample_json("mesorregioes")
        self.assertFalse(ibge.list_mesoregions().empty)

    @patch('seriesbr.helpers.lists.get_json')
    def test_list_cities(self, mocked_get_json):
        mocked_get_json.return_value = get_sample_json("municipios")
        self.assertFalse(ibge.list_cities().empty)

    @patch('seriesbr.helpers.lists.get_json')
    def test_list_states(self, mocked_get_json):
        mocked_get_json.return_value = get_sample_json("estados")
        self.assertFalse(ibge.list_states().empty)


if __name__ == "__main__":
    unittest.main()

# vi: nowrap
