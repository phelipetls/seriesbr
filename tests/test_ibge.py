import responses
import pandas as pd
import pytest

from freezegun import freeze_time
from responses import matchers
from seriesbr import ibge


@freeze_time("2021-12-31")
@responses.activate
@pytest.mark.parametrize(
    "kwargs,expected",
    [
        (
            {},
            {
                "url": "https://servicodados.ibge.gov.br/api/v3/agregados/1419/periodos/197001-202112/variaveis",
                "params": {"localidades": "BR", "view": "flat"},
            },
        ),
        (
            {"last_n": 5},
            {
                "url": "https://servicodados.ibge.gov.br/api/v3/agregados/1419/periodos/-5/variaveis",
                "params": {"localidades": "BR", "view": "flat"},
            },
        ),
        (
            {"start": "2019"},
            {
                "url": "https://servicodados.ibge.gov.br/api/v3/agregados/1419/periodos/201901-202112/variaveis",
                "params": {"localidades": "BR", "view": "flat"},
            },
        ),
        (
            {"start": "2019-11"},
            {
                "url": "https://servicodados.ibge.gov.br/api/v3/agregados/1419/periodos/201911-202112/variaveis",
                "params": {"localidades": "BR", "view": "flat"},
            },
        ),
        (
            {"start": "2019-11-07"},
            {
                "url": "https://servicodados.ibge.gov.br/api/v3/agregados/1419/periodos/201907-202112/variaveis",
                "params": {"localidades": "BR", "view": "flat"},
            },
        ),
        (
            {"end": "2019"},
            {
                "url": "https://servicodados.ibge.gov.br/api/v3/agregados/1419/periodos/197001-201912/variaveis",
                "params": {"localidades": "BR", "view": "flat"},
            },
        ),
        (
            {"end": "2019-11"},
            {
                "url": "https://servicodados.ibge.gov.br/api/v3/agregados/1419/periodos/197001-201911/variaveis",
                "params": {"localidades": "BR", "view": "flat"},
            },
        ),
        (
            {"end": "2019-11-07"},
            {
                "url": "https://servicodados.ibge.gov.br/api/v3/agregados/1419/periodos/197001-201907/variaveis",
                "params": {"localidades": "BR", "view": "flat"},
            },
        ),
        (
            {"start": "2019", "end": "2019"},
            {
                "url": "https://servicodados.ibge.gov.br/api/v3/agregados/1419/periodos/201901-201912/variaveis",
                "params": {"localidades": "BR", "view": "flat"},
            },
        ),
        (
            {"start": "2019-11", "end": "2019-11"},
            {
                "url": "https://servicodados.ibge.gov.br/api/v3/agregados/1419/periodos/201911-201911/variaveis",
                "params": {"localidades": "BR", "view": "flat"},
            },
        ),
        (
            {"start": "2019-11-07", "end": "2019-11-07"},
            {
                "url": "https://servicodados.ibge.gov.br/api/v3/agregados/1419/periodos/201907-201907/variaveis",
                "params": {"localidades": "BR", "view": "flat"},
            },
        ),
        (
            {"start": "2019-11-07", "end": "2019-11-07"},
            {
                "url": "https://servicodados.ibge.gov.br/api/v3/agregados/1419/periodos/201907-201907/variaveis",
                "params": {"localidades": "BR", "view": "flat"},
            },
        ),
        (
            {"start": "2019-11-07", "end": "2019-11-07"},
            {
                "url": "https://servicodados.ibge.gov.br/api/v3/agregados/1419/periodos/201907-201907/variaveis",
                "params": {"localidades": "BR", "view": "flat"},
            },
        ),
        (
            {"variables": 100},
            {
                "url": "https://servicodados.ibge.gov.br/api/v3/agregados/1419/periodos/197001-202112/variaveis/100",
                "params": {"localidades": "BR", "view": "flat"},
            },
        ),
        (
            {"variables": "100"},
            {
                "url": "https://servicodados.ibge.gov.br/api/v3/agregados/1419/periodos/197001-202112/variaveis/100",
                "params": {"localidades": "BR", "view": "flat"},
            },
        ),
        (
            {"variables": [1, 2, 3]},
            {
                "url": "https://servicodados.ibge.gov.br/api/v3/agregados/1419/periodos/197001-202112/variaveis/1|2|3",
                "params": {"localidades": "BR", "view": "flat"},
            },
        ),
        (
            {"brazil": True},
            {
                "url": "https://servicodados.ibge.gov.br/api/v3/agregados/1419/periodos/197001-202112/variaveis",
                "params": {"localidades": "BR", "view": "flat"},
            },
        ),
        (
            {"municipalities": True},
            {
                "url": "https://servicodados.ibge.gov.br/api/v3/agregados/1419/periodos/197001-202112/variaveis",
                "params": {"localidades": "N6", "view": "flat"},
            },
        ),
        (
            {"states": True},
            {
                "url": "https://servicodados.ibge.gov.br/api/v3/agregados/1419/periodos/197001-202112/variaveis",
                "params": {"localidades": "N3", "view": "flat"},
            },
        ),
        (
            {"macroregions": True},
            {
                "url": "https://servicodados.ibge.gov.br/api/v3/agregados/1419/periodos/197001-202112/variaveis",
                "params": {"localidades": "N2", "view": "flat"},
            },
        ),
        (
            {"mesoregions": True},
            {
                "url": "https://servicodados.ibge.gov.br/api/v3/agregados/1419/periodos/197001-202112/variaveis",
                "params": {"localidades": "N7", "view": "flat"},
            },
        ),
        (
            {"microregions": True},
            {
                "url": "https://servicodados.ibge.gov.br/api/v3/agregados/1419/periodos/197001-202112/variaveis",
                "params": {"localidades": "N9", "view": "flat"},
            },
        ),
        (
            {"states": [2, 3]},
            {
                "url": "https://servicodados.ibge.gov.br/api/v3/agregados/1419/periodos/197001-202112/variaveis",
                "params": {"localidades": "N3[2,3]", "view": "flat"},
            },
        ),
        (
            {"states": [2, 3], "municipalities": 3},
            {
                "url": "https://servicodados.ibge.gov.br/api/v3/agregados/1419/periodos/197001-202112/variaveis",
                "params": {"localidades": "N6[3]|N3[2,3]", "view": "flat"},
            },
        ),
        (
            {"classifications": 3},
            {
                "url": "https://servicodados.ibge.gov.br/api/v3/agregados/1419/periodos/197001-202112/variaveis",
                "params": {
                    "localidades": "BR",
                    "view": "flat",
                    "classificacao": "3[all]",
                },
            },
        ),
        (
            {"classifications": "3"},
            {
                "url": "https://servicodados.ibge.gov.br/api/v3/agregados/1419/periodos/197001-202112/variaveis",
                "params": {
                    "localidades": "BR",
                    "view": "flat",
                    "classificacao": "3[all]",
                },
            },
        ),
        (
            {"classifications": [1, 2]},
            {
                "url": "https://servicodados.ibge.gov.br/api/v3/agregados/1419/periodos/197001-202112/variaveis",
                "params": {
                    "localidades": "BR",
                    "view": "flat",
                    "classificacao": "1[all]|2[all]",
                },
            },
        ),
        (
            {"classifications": {1: [2], 3: [4, 5]}},
            {
                "url": "https://servicodados.ibge.gov.br/api/v3/agregados/1419/periodos/197001-202112/variaveis",
                "params": {
                    "localidades": "BR",
                    "view": "flat",
                    "classificacao": "1[2]|3[4,5]",
                },
            },
        ),
        (
            {"classifications": {1: []}},
            {
                "url": "https://servicodados.ibge.gov.br/api/v3/agregados/1419/periodos/197001-202112/variaveis",
                "params": {
                    "localidades": "BR",
                    "view": "flat",
                    "classificacao": "1[all]",
                },
            },
        ),
    ],
)
def test_ibge_get_series_url(kwargs, expected):
    expected_url = expected["url"]
    expected_params = expected["params"]

    responses.add(
        responses.GET,
        "https://servicodados.ibge.gov.br/api/v3/agregados/1419/metadados",
        json={"periodicidade": {"frequencia": "mensal"}},
        status=200,
    )

    responses.add(
        responses.GET,
        expected_url,
        match=[matchers.query_param_matcher(expected_params)],
        match_querystring=False,
        json=[
            {
                "V": "Valor",
                "D1C": "Brasil (Código)",
                "D2C": "Mês (Código)",
                "D3C": "Variável (Código)",
                "D3N": "Variável",
                "D4N": "Geral, grupo, subgrupo, item e subitem",
            },
            {
                "V": "0.56",
                "D1C": "1",
                "D2C": "201201",
                "D3C": "63",
                "D3N": "IPCA - Variação mensal",
                "D4N": "Índice geral",
            },
        ],
        status=200,
    )

    ibge.get_series(1419, **kwargs)


@freeze_time("2019-01-01")
@responses.activate
def test_get_series_dataframe():
    responses.add(
        responses.GET,
        "https://servicodados.ibge.gov.br/api/v3/agregados/1419/metadados",
        json={"periodicidade": {"frequencia": "mensal"}},
        status=200,
    )

    responses.add(
        responses.GET,
        "https://servicodados.ibge.gov.br/api/v3/agregados/1419/periodos/197001-201901/variaveis?localidades=BR&view=flat",
        json=[
            {
                "V": "Valor",
                "D1C": "Brasil (Código)",
                "D2C": "Mês (Código)",
                "D3C": "Variável (Código)",
                "D3N": "Variável",
                "D4N": "Geral, grupo, subgrupo, item e subitem",
            },
            {
                "V": "0.56",
                "D1C": "1",
                "D2C": "201201",
                "D3C": "63",
                "D3N": "IPCA - Variação mensal",
                "D4N": "Índice geral",
            },
        ],
        status=200,
    )

    df = ibge.get_series(1419)
    expected_df = pd.DataFrame(
        {
            "Valor": [0.56],
            "Brasil (Código)": ["1"],
            "Variável (Código)": ["63"],
            "Variável": ["IPCA - Variação mensal"],
            "Geral, grupo, subgrupo, item e subitem": ["Índice geral"],
        },
        index=pd.DatetimeIndex(["01/01/2012"], name="Date"),
    )

    pd.testing.assert_frame_equal(df, expected_df)


@responses.activate
def test_get_metadata():
    json = {
        "id": 1419,
        "nome": "nome",
        "URL": "URL",
        "pesquisa": "pesquisa",
        "assunto": "assunto",
        "periodicidade": "periodicidade",
        "nivelTerritorial": "nivelTerritorial",
        "variaveis": "variaveis",
        "classificacoes": "classificacoes",
    }

    responses.add(
        responses.GET,
        "https://servicodados.ibge.gov.br/api/v3/agregados/1419/metadados",
        json=json,
        status=200,
    )

    df = ibge.get_metadata(1419)
    expected_df = pd.DataFrame(
        {
            "values": json.values(),
        },
        index=pd.Index(json.keys()),
    )

    pd.testing.assert_frame_equal(df, expected_df)
