import pytest
import pandas as pd

from fixture_utils import read_json

from seriesbr import ibge

JSON = read_json("ibge_json.json")
METADATA = read_json("ibge_metadata.json")
SEARCH_RESULTS = read_json("ibge_search_results.json")


@pytest.fixture
def setup(mock_timeseries, mock_metadata, mock_search_results, mocker):
    mock_metadata(METADATA)
    mocker.patch("seriesbr.ibge.get_frequency", return_value="mensal")


@pytest.fixture
def mock_get_json(mocker):
    return mocker.patch("seriesbr.helpers.timeseries.get_json", return_value=JSON)


def test_timeseries_json_to_dataframe(setup, mock_get_json):
    df = ibge.get_series(1419, start="02-2017", end="04-2019")

    assert isinstance(df, pd.DataFrame)
    assert pd.api.types.is_datetime64_dtype(df.index)


periods = pd.DataFrame(
    {"valores": ["mensal", "201201", "201911"]}, index=["frequencia", "inicio", "fim"],
)


def test_get_frequency(mocker):
    mocker.patch("seriesbr.ibge.list_periods", return_value=periods)

    assert ibge.get_frequency(1419) == "mensal"


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


def test_metadata_json_to_dataframe(setup, mocker):
    df = ibge.get_metadata(1419)

    assert all([a == b for a, b in zip(df.index.tolist(), expected_indices)])


def test_build_metadata_url():
    url = ibge.build_metadata_url(1419)

    assert url == "https://servicodados.ibge.gov.br/api/v3/agregados/1419/metadados"


def test_search_json_parser(mocker):
    mocker.patch("seriesbr.helpers.request.get_json", return_value=SEARCH_RESULTS)

    df = ibge.search()

    assert isinstance(df, pd.DataFrame)
    assert not df.empty


def test_list_variables(mocker):
    m = mocker.patch(
        "seriesbr.ibge.request.get_json", return_value=read_json("ibge_variables.json")
    )
    df = ibge.list_variables(1419)

    assert not df.empty
    m.assert_called_with(
        "https://servicodados.ibge.gov.br/api/v3/"
        "agregados/1419/variaveis/all?localidades=BR"
    )


expected_locations = [
    "brazil",
    "macroregions",
    "microregions",
    "municipalities",
    "mesoregions",
    "states",
]


def test_list_locations(mocker):
    m = mocker.patch(
        "seriesbr.ibge.request.get_json", return_value=read_json("ibge_metadata.json")
    )

    df = ibge.list_locations(1419)

    assert df.locations.tolist() == expected_locations

    m.assert_called_with(
        "https://servicodados.ibge.gov.br/api/v3" "/agregados/1419/metadados"
    )


expected_periods = ["frequencia", "inicio", "fim"]


def test_list_periods(mocker):
    mocker.patch(
        "seriesbr.helpers.metadata.get_json",
        return_value=read_json("ibge_metadata.json"),
    )
    df = ibge.list_periods(1419)

    assert df.index.tolist() == expected_periods
