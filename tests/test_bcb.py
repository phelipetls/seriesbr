import re
import pytest
import responses
import pandas as pd

from seriesbr import bcb
from fixture_utils import read_json

SERIES_JSON = read_json("bcb_json.json")
METADATA = read_json("bcb_metadata.json")
SEARCH_RESULTS = read_json("bcb_search_results.json")


@responses.activate
def test_get_series():
    responses.add(
        responses.GET,
        "https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados",
        json=SERIES_JSON,
        status=200,
    )

    df = bcb.get_series({"Selic": 11})

    assert isinstance(df, pd.DataFrame)
    assert df.columns.tolist() == ["Selic"]
    assert pd.api.types.is_datetime64_dtype(df.index)
    assert pd.api.types.is_float_dtype(df.values)


@responses.activate
def test_get_metadata():
    responses.add(
        responses.GET,
        "https://dadosabertos.bcb.gov.br/api/3/action/package_search?fq=codigo_sgs:20786",
        json=METADATA,
        status=200,
    )

    df = bcb.get_metadata(20786)

    assert not df.empty


@responses.activate
def test_search():
    responses.add(
        responses.GET,
        "https://dadosabertos.bcb.gov.br/api/3/action/package_search?q=Selic&rows=10&start=1&sort=score desc",
        json=SEARCH_RESULTS,
        status=200,
    )

    df = bcb.search("Selic")

    assert df.columns.tolist() == [
        "codigo_sgs",
        "title",
        "periodicidade",
        "unidade_medida",
    ]
