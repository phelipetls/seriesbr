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
        test = ibge.list_locations(1419).parameters.tolist()
        expected = [
            "brazil",
            "macroregion",
            "microregion",
            "municipality",
            "mesoregion",
            "state",
        ]
        self.assertListEqual(test, expected)

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
        test = ibge.get_frequency(1419)
        expected = "anual"
        self.assertEqual(test, expected)

    def tearDown(self):
        patch.stopall()


@patch("seriesbr.helpers.lists.get_json")
class TestListRegionsFunctions(unittest.TestCase):
    """Test list regions functions"""

    def test_list_macroregions(self, mocked_get_json):
        mocked_get_json.return_value = get_sample_json("ibge_regioes.json")

        df = ibge.list_macroregions()
        self.assertFalse(df.empty)

    def test_list_microregions(self, mocked_get_json):
        mocked_get_json.return_value = get_sample_json("ibge_microrregioes.json")

        df = ibge.list_microregions()
        self.assertFalse(df.empty)

    def test_list_mesoregions(self, mocked_get_json):
        mocked_get_json.return_value = get_sample_json("ibge_mesorregioes.json")

        df = ibge.list_mesoregions()
        self.assertFalse(df.empty)

    def test_list_cities(self, mocked_get_json):
        mocked_get_json.return_value = get_sample_json("ibge_municipios.json")

        df = ibge.list_cities()
        self.assertFalse(df.empty)

    def test_list_states(self, mocked_get_json):
        mocked_get_json.return_value = get_sample_json("ibge_estados.json")

        df = ibge.list_states()
        self.assertFalse(df.empty)


if __name__ == "__main__":
    unittest.main(failfast=True)

# vi: nowrap
