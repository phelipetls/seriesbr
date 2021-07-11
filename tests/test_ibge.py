import pytest
import responses
import pandas as pd
from freezegun import freeze_time

from fixture_utils import read_json

from seriesbr import ibge

METADATA = read_json("ibge_metadata.json")
SERIES_JSON = read_json("ibge_json.json")
SEARCH_RESULTS = read_json("ibge_search_results.json")


@freeze_time("2019-01-01")
@responses.activate
def test_get_series():
    responses.add(
        responses.GET,
        "https://servicodados.ibge.gov.br/api/v3/agregados/1419/metadados",
        json=METADATA,
        status=200,
    )

    responses.add(
        responses.GET,
        "https://servicodados.ibge.gov.br/api/v3/agregados/1419/periodos/197001-201901/variaveis",
        json=SERIES_JSON,
        status=200,
    )

    df = ibge.get_series(1419)

    assert isinstance(df, pd.DataFrame)
    assert pd.api.types.is_datetime64_dtype(df.index)


@responses.activate
def test_get_metadata():
    responses.add(
        responses.GET,
        "https://servicodados.ibge.gov.br/api/v3/agregados/1419/metadados",
        json=METADATA,
        status=200,
    )

    df = ibge.get_metadata(1419)

    assert all(
        [
            actual == expected
            for actual, expected in zip(
                df.index.tolist(),
                [
                    "id",
                    "nome",
                    "URL",
                    "pesquisa",
                    "assunto",
                    "periodicidade",
                    "nivelTerritorial",
                    "variaveis",
                    "classificacoes",
                ],
            )
        ]
    )


@responses.activate
def test_search():
    responses.add(
        responses.GET,
        "https://servicodados.ibge.gov.br/api/v3/agregados/",
        json=SEARCH_RESULTS,
        status=200,
    )

    df = ibge.search("Selic")

    assert all("Selic" in value for value in df.values)
