import pytest
import pandas as pd

from seriesbr import ipea

from fixture_utils import read_json

JSON = read_json("ipea_json.json")
METADATA = read_json("ipea_metadata.json")
SEARCH_RESULTS = read_json("ipea_search_results.json")


@pytest.fixture
def setup(mock_timeseries, mock_metadata, mock_search_results):
    mock_timeseries(JSON)
    mock_metadata(METADATA)
    mock_search_results(METADATA)


def test_timeseries_json_to_dataframe(setup):
    df = ipea.get_series({"Selic": "BM12_CRLIN12"})

    assert isinstance(df, pd.DataFrame)
    assert pd.api.types.is_datetime64_dtype(df.index)
    assert pd.api.types.is_float_dtype(df.values)
    assert df.columns.tolist() == ["Selic"]


def test_url(setup):
    url = ipea.build_metadata_url("BM12_CRLIN12")
    expected_url = (
        "http://ipeadata2-homologa.ipea.gov.br/api/v1/Metadados('BM12_CRLIN12')"
    )
    assert url == expected_url


def test_dataframe(setup):
    assert not ipea.get_metadata(21789).empty


def test_search_results_dataframe(setup):
    df = ipea.search("Selic")
    assert not df.empty


to_patch = "seriesbr.helpers.lists.get_json"


def test_list_themes(mocker):
    mocker.patch(to_patch).return_value = read_json("ipea_temas.json")

    columns = ipea.list_themes().columns.tolist()
    expected_columns = ["TEMCODIGO", "TEMCODIGO_PAI", "TEMNOME"]

    assert [a == b for (a, b) in zip(columns, expected_columns)]


def test_list_countries(mocker):
    mocker.patch(to_patch).return_value = read_json("ipea_paises.json")

    columns = ipea.list_countries().columns.tolist()
    expected_columns = ["PAICODIGO", "PAINOME"]

    assert [a == b for (a, b) in zip(columns, expected_columns)]


def test_list_metadata():
    pd.testing.assert_index_equal(
        ipea.list_metadata().index,
        pd.Index(
            [
                "SERNOME",
                "SERCODIGO",
                "PERNOME",
                "UNINOME",
                "BASNOME",
                "TEMCODIGO",
                "PAICODIGO",
                "SERCOMENTARIO",
                "FNTNOME",
                "FNTSIGLA",
                "FNTURL",
                "MULNOME",
                "SERATUALIZACAO",
                "SERSTATUS",
                "SERNUMERICA",
            ]
        ),
    )
