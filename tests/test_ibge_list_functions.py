import os
import sys
import json
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from seriesbr import ibge


def get_sample_json(filename):
    json_path = Path(__file__).resolve().parent / "sample_jsons" / filename
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

    @patch('seriesbr.helpers.metadata.get_json')
    def test_list_classifications(self, mocked_get_metadata):
        mocked_get_metadata.return_value = get_sample_json("ibge_metadata")
        test = ibge.list_classifications(1419).columns.tolist()
        correct = ['id', 'nome', 'unidade', 'nivel', 'classificacao_id', 'classificacao_nome']
        self.assertListEqual(test, correct)

    @patch('seriesbr.helpers.metadata.get_json')
    def test_list_periods(self, mocked_get_metadata):
        mocked_get_metadata.return_value = get_sample_json("ibge_metadata")
        test = ibge.list_periods(1419).index.tolist()
        correct = ["frequencia", "inicio", "fim"]
        self.assertListEqual(test, correct)


class TestListRegionsFunctions(unittest.TestCase):

    @patch('seriesbr.helpers.lists.get_json')
    def test_list_macroregions(self, mocked_get_json):
        mocked_get_json.return_value = get_sample_json("ibge_regioes")
        self.assertFalse(ibge.list_macroregions().empty)

    @patch('seriesbr.helpers.lists.get_json')
    def test_list_microregions(self, mocked_get_json):
        mocked_get_json.return_value = get_sample_json("ibge_microrregioes")
        self.assertFalse(ibge.list_microregions().empty)

    @patch('seriesbr.helpers.lists.get_json')
    def test_list_mesoregions(self, mocked_get_json):
        mocked_get_json.return_value = get_sample_json("ibge_mesorregioes")
        self.assertFalse(ibge.list_mesoregions().empty)

    @patch('seriesbr.helpers.lists.get_json')
    def test_list_cities(self, mocked_get_json):
        mocked_get_json.return_value = get_sample_json("ibge_municipios")
        self.assertFalse(ibge.list_cities().empty)

    @patch('seriesbr.helpers.lists.get_json')
    def test_list_states(self, mocked_get_json):
        mocked_get_json.return_value = get_sample_json("ibge_estados")
        self.assertFalse(ibge.list_states().empty)


if __name__ == "__main__":
    unittest.main()

# vi: nowrap
