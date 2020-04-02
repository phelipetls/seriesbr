import os
import sys
import unittest

from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from seriesbr import ibge  # noqa: E402
from mock_helpers import get_sample_json, mock_json  # noqa: E402


class TestListVariablesFunction(unittest.TestCase):
    def setUp(self):
        mock_json(
            path="seriesbr.ibge.get_json", json=get_sample_json("ibge_variables.json")
        ).start()

    def test_ibge_list_variables(self):
        self.assertFalse(ibge.list_variables(1419).empty)

    def tearDown(self):
        patch.stopall()


class TestListMetadataFunctions(unittest.TestCase):
    def setUp(self):
        # simulate getting a JSON response from a search query
        mock_json(
            path="seriesbr.ibge.get_json", json=get_sample_json("ibge_metadata.json")
        ).start()

        # simulate getting a JSON response from a metadata query
        mock_json(
            path="seriesbr.helpers.metadata.get_json",
            json=get_sample_json("ibge_metadata.json"),
        ).start()

    def test_ibge_list_locations(self):
        self.assertFalse(ibge.list_locations(1419).empty)

    def test_list_classifications(self):
        test = ibge.list_classifications(1419).columns.tolist()
        expected = [
            "id",
            "nome",
            "unidade",
            "nivel",
            "classificacao_id",
            "classificacao_nome",
        ]
        self.assertListEqual(test, expected)

    def test_list_periods(self):
        test = ibge.list_periods(1419).index.tolist()
        expected = ["frequencia", "inicio", "fim"]
        self.assertListEqual(test, expected)

    def test_get_frequency(self):
        test = "anual"
        expected = ibge.get_frequency(1419)
        self.assertEqual(test, expected)

    def tearDown(self):
        patch.stopall()


@patch("seriesbr.helpers.lists.get_json")
class TestListRegionsFunctions(unittest.TestCase):
    """Test list regions functions"""

    def test_list_macroregions(self, mocked_get_json):
        mocked_get_json.return_value = get_sample_json("ibge_regioes.json")
        self.assertFalse(ibge.list_macroregions().empty)

    def test_list_microregions(self, mocked_get_json):
        mocked_get_json.return_value = get_sample_json("ibge_microrregioes.json")
        self.assertFalse(ibge.list_microregions().empty)

    def test_list_mesoregions(self, mocked_get_json):
        mocked_get_json.return_value = get_sample_json("ibge_mesorregioes.json")
        self.assertFalse(ibge.list_mesoregions().empty)

    def test_list_cities(self, mocked_get_json):
        mocked_get_json.return_value = get_sample_json("ibge_municipios.json")
        self.assertFalse(ibge.list_cities().empty)

    def test_list_states(self, mocked_get_json):
        mocked_get_json.return_value = get_sample_json("ibge_estados.json")
        self.assertFalse(ibge.list_states().empty)


if __name__ == "__main__":
    unittest.main(failfast=True)

# vi: nowrap
