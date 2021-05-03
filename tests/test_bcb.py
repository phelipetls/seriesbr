import pytest
import pandas as pd

from seriesbr import bcb
from fixture_utils import read_json

JSON = read_json("bcb_json.json")
METADATA = read_json("bcb_metadata.json")
SEARCH_RESULTS = read_json("bcb_search_results.json")


@pytest.fixture
def setup(mock_timeseries, mock_metadata, mock_search_results):
    mock_timeseries(JSON)
    mock_metadata(METADATA)
    mock_search_results(METADATA)


def test_timeseries_json_to_dataframe(setup):
    df = bcb.get_series({"Selic": 11})

    assert isinstance(df, pd.DataFrame)
    assert df.columns.tolist() == ["Selic"]
    assert pd.api.types.is_datetime64_dtype(df.index)
    assert pd.api.types.is_float_dtype(df.values)


def test_metadata_url():
    url = bcb.build_metadata_url(20786)

    expected_url = (
        "https://dadosabertos.bcb.gov.br/api/3/action/"
        "package_search?fq=codigo_sgs:20786"
    )

    assert url == expected_url


def test_metadata_dataframe(setup):
    df = bcb.get_metadata(20786)

    assert not df.empty


BASEURL = "https://dadosabertos.bcb.gov.br/api/3/action/package_search?"


def test_search_bcb():
    url = bcb.build_search_url("spread")

    assert url == BASEURL + "q=spread&rows=10&start=1&sort=score desc"


def test_search_multiple_strings():
    url = bcb.build_search_url("spread", "mensal", "livre")

    assert url == BASEURL + "q=spread&rows=10&start=1&sort=score desc&fq=mensal+livre"


def test_search_with_pagination():
    url = bcb.build_search_url("spread", "mensal", "livre", rows=30, start=5)

    assert url == BASEURL + "q=spread&rows=30&start=5&sort=score desc&fq=mensal+livre"


def test_search_results(setup):
    df = bcb.search("Selic")

    assert df.columns.tolist() == [
        "codigo_sgs",
        "title",
        "periodicidade",
        "unidade_medida",
    ]
