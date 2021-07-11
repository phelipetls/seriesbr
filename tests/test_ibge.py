import responses
import pandas as pd
from freezegun import freeze_time

from seriesbr import ibge


@freeze_time("2019-01-01")
@responses.activate
def test_get_series():
    responses.add(
        responses.GET,
        "https://servicodados.ibge.gov.br/api/v3/agregados/1419/metadados",
        json={
            "id": 1419,
            "nome": "IPCA",
            "URL": "http://sidra.ibge.gov.br/tabela/1419",
            "pesquisa": "Índice Nacional de Preços ao Consumidor Amplo",
            "assunto": "Índices de preços",
            "periodicidade": {"frequencia": "mensal", "inicio": 201201, "fim": 201912},
            "nivelTerritorial": {
                "Administrativo": ["N1", "N6", "N7"],
            },
            "variaveis": [{"id": 1, "nome": "IPCA - Variação mensal", "unidade": "%"}],
            "classificacoes": [
                {
                    "id": 315,
                    "nome": "Geral, grupo, subgrupo, item e subitem",
                    "categorias": [
                        {
                            "id": 7169,
                            "nome": "Índice geral",
                        }
                    ],
                }
            ],
        },
        status=200,
    )

    responses.add(
        responses.GET,
        "https://servicodados.ibge.gov.br/api/v3/agregados/1419/periodos/197001-201901/variaveis?localidades=BR&view=flat",
        json=[
            {
                "NC": "Nível Territorial (Código)",
                "NN": "Nível Territorial",
                "MC": "Unidade de Medida (Código)",
                "MN": "Unidade de Medida",
                "V": "Valor",
                "D1C": "Brasil (Código)",
                "D1N": "Brasil",
                "D2C": "Mês (Código)",
                "D2N": "Mês",
                "D3C": "Variável (Código)",
                "D3N": "Variável",
                "D4C": "Geral, grupo, subgrupo, item e subitem (Código)",
                "D4N": "Geral, grupo, subgrupo, item e subitem",
            },
            {
                "NC": "1",
                "NN": "Brasil",
                "MC": "2",
                "MN": "%",
                "V": "0.56",
                "D1C": "1",
                "D1N": "Brasil",
                "D2C": "201201",
                "D2N": "janeiro 2012",
                "D3C": "63",
                "D3N": "IPCA - Variação mensal",
                "D4C": "7169",
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


@responses.activate
def test_search():
    responses.add(
        responses.GET,
        "https://servicodados.ibge.gov.br/api/v3/agregados/",
        json=[
            {
                "id": "1",
                "nome": "Nome da pesquisa",
                "agregados": [
                    {
                        "id": "1000",
                        "nome": "Selic",
                    }
                ],
            }
        ],
        status=200,
    )

    df = ibge.search("Selic")

    assert all("Selic" in value for value in df.values)
