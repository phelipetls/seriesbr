import unittest
import pandas as pd

from seriesbr import ibge
from unittest.mock import patch
from mock_helpers import get_sample_json


settings = {"return_value": get_sample_json("ibge_json.json")}


@patch("seriesbr.helpers.timeseries.get_json", **settings)
class TestIbgeJsonParser(unittest.TestCase):
    """Test conversion of IBGE timeseries JSON into DataFrame and related functions"""

    # don't make a request to get frequency
    @patch("seriesbr.ibge.get_frequency", return_value="mensal")
    def test_timeseries_json_to_dataframe(self, _, f):
        df = ibge.get_series(1419, start="02-2017", end="04-2019")

        self.assertIsInstance(df, pd.DataFrame)
        self.assertTrue(pd.api.types.is_datetime64_dtype(df.index))

        f.assert_called_with(
            "https://servicodados.ibge.gov.br/api/v3/"
            "agregados/1419/"
            "periodos/201702-201904/"
            "variaveis?&localidades=BR&view=flat"
        )


periods = pd.DataFrame(
    {"valores": ["mensal", "201201", "201911"]}, index=["frequencia", "inicio", "fim"],
)


class TestIbgeGetFrequency(unittest.TestCase):
    """Test if get_frequency returns the right thing"""

    @patch("seriesbr.ibge.list_periods")
    def test_get_frequency(self, f):
        f.return_value = periods

        test = ibge.get_frequency(1419)
        expected = "mensal"
        self.assertEqual(test, expected)


settings = {"return_value": get_sample_json("ibge_metadata.json")}


@patch("seriesbr.helpers.metadata.get_json", **settings)
class TestIbgeGetMetadata(unittest.TestCase):
    """Test conversion of IBGE metadata JSON into DataFrame"""

    expected_indices = [
        "id",
        "nome",
        "URL",
        "pesquisa",
        "assunto",
        "periodicidade",
        "nivelTerritorial",
        "variaveis",
        "classificacoes",
    ]

    def test_metadata_json_to_dataframe(self, _):
        df = ibge.get_metadata(1419)
        self.assertListEqual(df.index.tolist(), self.expected_indices)

    def test_url(self, f):
        expected_url = (
            "https://servicodados.ibge.gov.br/api/v3/agregados/1419/metadados"
        )

        ibge.get_metadata(1419)
        f.assert_called_with(expected_url)


settings = {"return_value": get_sample_json("ibge_search_results.json")}


@patch("seriesbr.ibge.request.get_json", **settings)
class TestIbgeSearch(unittest.TestCase):
    """Test if IBGE parses IBGE's API JSON response correctly"""

    def test_search_json_parser(self, _):
        df = ibge.search()
        self.assertIsInstance(df, pd.DataFrame)

    def test_if_dataframe_is_not_empty(self, _):
        df = ibge.search()
        self.assertFalse(df.empty)


settings = {"return_value": get_sample_json("ibge_variables.json")}


@patch("seriesbr.ibge.request.get_json", **settings)
class TestIbgeListVariables(unittest.TestCase):
    """Test IBGE list variables function"""

    def test_list_variables(self, _):
        df = ibge.list_variables(1419)

        self.assertFalse(df.empty)

    def test_url(self, f):
        ibge.list_variables(1419)

        f.assert_called_with(
            "https://servicodados.ibge.gov.br/api/v3/"
            "agregados/1419/variaveis/all?localidades=BR"
        )


settings = {"return_value": get_sample_json("ibge_metadata.json")}


@patch("seriesbr.ibge.request.get_json", **settings)
class TestIbgeListLocations(unittest.TestCase):
    """Test IBGE list locations function"""

    expected_locations = [
        "brazil",
        "macroregions",
        "microregions",
        "municipalities",
        "mesoregions",
        "states",
    ]

    def test_list(self, _):
        df = ibge.list_locations(1419)

        locations = df.locations.tolist()
        self.assertEqual(locations, self.expected_locations)

    def test_url(self, f):
        ibge.list_locations(1419)
        f.assert_called_with(
            "https://servicodados.ibge.gov.br/api/v3" "/agregados/1419/metadados"
        )


@patch("seriesbr.helpers.metadata.get_json", **settings)
class TestIbgeListPeriods(unittest.TestCase):
    """Test IBGE list periods function"""

    expected_indices = ["frequencia", "inicio", "fim"]

    def test_list(self, _):
        df = ibge.list_periods(1419)

        indices = df.index.tolist()
        self.assertListEqual(indices, self.expected_indices)


@patch("seriesbr.helpers.metadata.get_json", **settings)
class TestIbgeListClassifications(unittest.TestCase):
    """Test IBGE list classifications function"""

    expected_columns = [
        "id",
        "nome",
        "unidade",
        "nivel",
        "classificacao_id",
        "classificacao_nome",
    ]

    def test_list(self, _):
        df = ibge.list_classifications(1419)

        columns = df.columns.tolist()
        self.assertEqual(columns, self.expected_columns)


regions = {
    "list_macroregions": "ibge_macrorregioes.json",
    "list_microregions": "ibge_microrregioes.json",
    "list_mesoregions": "ibge_mesorregioes.json",
    "list_municipalities": "ibge_municipios.json",
    "list_states": "ibge_estados.json",
}


@patch("seriesbr.helpers.lists.get_json")
class TestListRegionsFunctions(unittest.TestCase):
    """Test list regions functions"""

    def test_list_regions(self, m):
        for region in regions:
            with self.subTest(region=region):
                m.return_value = get_sample_json(regions[region])
                function = getattr(ibge, region)

                df = function()
                self.assertFalse(df.empty)


if __name__ == "__main__":
    unittest.main(failfast=True)
