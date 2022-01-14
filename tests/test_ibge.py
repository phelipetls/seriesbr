import requests
import responses
import pandas as pd
import pytest

from freezegun import freeze_time
from responses import matchers
from seriesbr import ibge

BASE_URL = "https://servicodados.ibge.gov.br/api/v3/agregados/1419"


@pytest.fixture
def mock_get_metadata():
    def _mock_get_metadata(metadata):
        responses.add(
            responses.GET,
            BASE_URL + "/metadados",
            json=metadata,
            status=200,
        )

    return _mock_get_metadata


@freeze_time("2021-12-31")
@responses.activate
@pytest.mark.parametrize(
    "kwargs,expected",
    [
        (
            {},
            {
                "url": BASE_URL + "/periodos/197001-202112/variaveis",
                "params": {},
            },
        ),
        (
            {"last_n": 5},
            {
                "url": BASE_URL + "/periodos/-5/variaveis",
                "params": {},
            },
        ),
        (
            {"start": "2019"},
            {
                "url": BASE_URL + "/periodos/201901-202112/variaveis",
                "params": {},
            },
        ),
        (
            {"start": "2019-11"},
            {
                "url": BASE_URL + "/periodos/201911-202112/variaveis",
                "params": {},
            },
        ),
        (
            {"start": "2019-11-07"},
            {
                "url": BASE_URL + "/periodos/201911-202112/variaveis",
                "params": {},
            },
        ),
        (
            {"end": "2019"},
            {
                "url": BASE_URL + "/periodos/197001-201912/variaveis",
                "params": {},
            },
        ),
        (
            {"end": "2019-11"},
            {
                "url": BASE_URL + "/periodos/197001-201911/variaveis",
                "params": {},
            },
        ),
        (
            {"end": "2019-11-07"},
            {
                "url": BASE_URL + "/periodos/197001-201911/variaveis",
                "params": {},
            },
        ),
        (
            {"start": "2019", "end": "2019"},
            {
                "url": BASE_URL + "/periodos/201901-201912/variaveis",
                "params": {},
            },
        ),
        (
            {"start": "2019-11", "end": "2019-11"},
            {
                "url": BASE_URL + "/periodos/201911-201911/variaveis",
                "params": {},
            },
        ),
        (
            {"start": "2019-11-07", "end": "2019-11-07"},
            {
                "url": BASE_URL + "/periodos/201911-201911/variaveis",
                "params": {},
            },
        ),
        (
            {"variables": 100},
            {
                "url": BASE_URL + "/periodos/197001-202112/variaveis/100",
                "params": {},
            },
        ),
        (
            {"variables": "100"},
            {
                "url": BASE_URL + "/periodos/197001-202112/variaveis/100",
                "params": {},
            },
        ),
        (
            {"variables": [1, 2, 3]},
            {
                "url": BASE_URL + "/periodos/197001-202112/variaveis/1|2|3",
                "params": {},
            },
        ),
        (
            {"brazil": True},
            {
                "url": BASE_URL + "/periodos/197001-202112/variaveis",
                "params": {"localidades": "BR"},
            },
        ),
        (
            {"municipalities": True},
            {
                "url": BASE_URL + "/periodos/197001-202112/variaveis",
                "params": {"localidades": "N6"},
            },
        ),
        (
            {"states": True},
            {
                "url": BASE_URL + "/periodos/197001-202112/variaveis",
                "params": {"localidades": "N3"},
            },
        ),
        (
            {"macroregions": True},
            {
                "url": BASE_URL + "/periodos/197001-202112/variaveis",
                "params": {"localidades": "N2"},
            },
        ),
        (
            {"mesoregions": True},
            {
                "url": BASE_URL + "/periodos/197001-202112/variaveis",
                "params": {"localidades": "N7"},
            },
        ),
        (
            {"microregions": True},
            {
                "url": BASE_URL + "/periodos/197001-202112/variaveis",
                "params": {"localidades": "N9"},
            },
        ),
        (
            {"states": [2, 3]},
            {
                "url": BASE_URL + "/periodos/197001-202112/variaveis",
                "params": {"localidades": "N3[2,3]"},
            },
        ),
        (
            {"states": [2, 3], "municipalities": 3},
            {
                "url": BASE_URL + "/periodos/197001-202112/variaveis",
                "params": {"localidades": "N6[3]|N3[2,3]"},
            },
        ),
        (
            {"classifications": 3},
            {
                "url": BASE_URL + "/periodos/197001-202112/variaveis",
                "params": {"classificacao": "3[all]"},
            },
        ),
        (
            {"classifications": "3"},
            {
                "url": BASE_URL + "/periodos/197001-202112/variaveis",
                "params": {"classificacao": "3[all]"},
            },
        ),
        (
            {"classifications": [1, 2]},
            {
                "url": BASE_URL + "/periodos/197001-202112/variaveis",
                "params": {"classificacao": "1[all]|2[all]"},
            },
        ),
        (
            {"classifications": {1: [2], 3: [4, 5]}},
            {
                "url": BASE_URL + "/periodos/197001-202112/variaveis",
                "params": {"classificacao": "1[2]|3[4,5]"},
            },
        ),
        (
            {"classifications": {1: []}},
            {
                "url": BASE_URL + "/periodos/197001-202112/variaveis",
                "params": {"classificacao": "1[all]"},
            },
        ),
    ],
)
def test_ibge_get_monthly_series_url(kwargs, expected, mock_get_metadata):
    mock_get_metadata(
        {
            "periodicidade": {"frequencia": "mensal"},
            "nivelTerritorial": {
                "Administrativo": ["N6", "N3", "N2", "N7", "N9", "N1"]
            },
        }
    )

    expected_url = expected["url"]
    expected_params = expected["params"]

    responses.add(
        responses.GET,
        expected_url,
        match=[
            matchers.query_param_matcher(
                {"localidades": "BR", "view": "flat", **expected_params}
            )
        ],
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


@freeze_time("2021-12-31")
@responses.activate
@pytest.mark.parametrize(
    "kwargs,expected",
    [
        (
            {"start": "2019"},
            {
                "url": BASE_URL + "/periodos/201901-202104/variaveis",
                "params": {},
            },
        ),
        (
            {"start": "2019-11"},
            {
                "url": BASE_URL + "/periodos/201904-202104/variaveis",
                "params": {},
            },
        ),
        (
            {"start": "2019-11-07"},
            {
                "url": BASE_URL + "/periodos/201904-202104/variaveis",
                "params": {},
            },
        ),
        (
            {"end": "2019"},
            {
                "url": BASE_URL + "/periodos/197001-201904/variaveis",
                "params": {},
            },
        ),
        (
            {"end": "2019-11"},
            {
                "url": BASE_URL + "/periodos/197001-201904/variaveis",
                "params": {},
            },
        ),
        (
            {"end": "2019-11-07"},
            {
                "url": BASE_URL + "/periodos/197001-201904/variaveis",
                "params": {},
            },
        ),
    ],
)
def test_ibge_get_quarterly_series_url(kwargs, expected, mock_get_metadata):
    mock_get_metadata({"periodicidade": {"frequencia": "trimestral"}})

    expected_url = expected["url"]
    expected_params = expected["params"]

    responses.add(
        responses.GET,
        expected_url,
        match=[
            matchers.query_param_matcher(
                {"localidades": "BR", "view": "flat", **expected_params}
            )
        ],
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


@freeze_time("2021-12-31")
@responses.activate
@pytest.mark.parametrize(
    "kwargs,expected",
    [
        (
            {"start": "2019"},
            {
                "url": BASE_URL + "/periodos/2019-2021/variaveis",
                "params": {},
            },
        ),
        (
            {"start": "2019-11"},
            {
                "url": BASE_URL + "/periodos/2019-2021/variaveis",
                "params": {},
            },
        ),
        (
            {"start": "2019-11-07"},
            {
                "url": BASE_URL + "/periodos/2019-2021/variaveis",
                "params": {},
            },
        ),
        (
            {"end": "2019"},
            {
                "url": BASE_URL + "/periodos/1970-2019/variaveis",
                "params": {},
            },
        ),
        (
            {"end": "2019-11"},
            {
                "url": BASE_URL + "/periodos/1970-2019/variaveis",
                "params": {},
            },
        ),
        (
            {"end": "2019-11-07"},
            {
                "url": BASE_URL + "/periodos/1970-2019/variaveis",
                "params": {},
            },
        ),
    ],
)
def test_ibge_get_yearly_series_url_and_dataframe(kwargs, expected, mock_get_metadata):
    expected_url = expected["url"]
    expected_params = expected["params"]

    mock_get_metadata({"periodicidade": {"frequencia": "anual"}})

    expected_url = expected["url"]
    expected_params = expected["params"]

    responses.add(
        responses.GET,
        expected_url,
        match=[
            matchers.query_param_matcher(
                {"localidades": "BR", "view": "flat", **expected_params}
            )
        ],
        match_querystring=False,
        json=[
            {
                "V": "Valor",
                "D1C": "Brasil (Código)",
                "D2C": "Ano (Código)",
                "D3C": "Variável (Código)",
                "D3N": "Variável",
                "D4N": "Geral, grupo, subgrupo, item e subitem",
            },
            {
                "V": "0.56",
                "D1C": "1",
                "D2C": "2012",
                "D3C": "63",
                "D3N": "IPCA - Variação mensal",
                "D4N": "Índice geral",
            },
        ],
        status=200,
    )

    df = ibge.get_series(1419, **kwargs)
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


@freeze_time("2019-01-01")
@responses.activate
def test_get_series_dataframe(mock_get_metadata):
    mock_get_metadata({"periodicidade": {"frequencia": "mensal"}})

    responses.add(
        responses.GET,
        BASE_URL + "/periodos/197001-201901/variaveis?localidades=BR&view=flat",
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
@freeze_time("2021-12-31")
def test_ibge_get_quarterly_series_dataframe(mock_get_metadata):
    mock_get_metadata({"periodicidade": {"frequencia": "trimestral"}})

    responses.add(
        responses.GET,
        BASE_URL + "/periodos/197001-202104/variaveis",
        match=[matchers.query_param_matcher({"localidades": "BR", "view": "flat"})],
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
            {
                "V": "0.56",
                "D1C": "1",
                "D2C": "201202",
                "D3C": "63",
                "D3N": "IPCA - Variação mensal",
                "D4N": "Índice geral",
            },
            {
                "V": "0.56",
                "D1C": "1",
                "D2C": "201203",
                "D3C": "63",
                "D3N": "IPCA - Variação mensal",
                "D4N": "Índice geral",
            },
            {
                "V": "0.56",
                "D1C": "1",
                "D2C": "201204",
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
            "Valor": [0.56] * 4,
            "Brasil (Código)": ["1"] * 4,
            "Variável (Código)": ["63"] * 4,
            "Variável": ["IPCA - Variação mensal"] * 4,
            "Geral, grupo, subgrupo, item e subitem": ["Índice geral"] * 4,
        },
        index=pd.DatetimeIndex(
            ["2012-01-01", "2012-04-01", "2012-07-01", "2012-10-01"], name="Date"
        ),
    )

    pd.testing.assert_frame_equal(df, expected_df)


@freeze_time("2021-12-31")
@responses.activate
def test_ibge_get_series_internal_server_error_message(capsys, mock_get_metadata):
    mock_get_metadata({"periodicidade": {"frequencia": "mensal"}})

    responses.add(
        responses.GET,
        BASE_URL + "/periodos/197001-202112/variaveis",
        match=[matchers.query_param_matcher({"localidades": "BR", "view": "flat"})],
        status=500,
    )

    with pytest.raises(requests.exceptions.HTTPError):
        ibge.get_series(1419)
        captured = capsys.readouterr()
        assert captured.out == (
            "A consulta pode ter retornado mais que 100.000 linhas. "
            "Tente adicionar mais filtros.\n"
        )


@freeze_time("2021-12-31")
@responses.activate
def test_ibge_get_series_forbidden_location_filter(capsys, mock_get_metadata):
    mock_get_metadata(
        {
            "periodicidade": {"frequencia": "mensal"},
            "nivelTerritorial": {"Administrativo": ["N1", "N3"]},
        }
    )

    responses.add(
        responses.GET,
        BASE_URL + "/periodos/197001-202104/variaveis",
        match=[matchers.query_param_matcher({"localidades": "BR", "view": "flat"})],
        status=500,
    )

    with pytest.raises(ValueError):
        ibge.get_series(1419, municipalities=True)
        captured = capsys.readouterr()
        assert captured.out == (
            "Você está tentando filtrar a tabela pela localidade 'municipalities', "
            "mas somente as localidades 'brazil, states' são permitidas."
        )


@responses.activate
def test_ibge_get_metadata(mock_get_metadata):
    json = {
        "id": 1419,
    }

    mock_get_metadata(json)

    assert ibge.get_metadata(1419) == json
