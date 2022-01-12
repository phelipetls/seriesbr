import responses
import pandas as pd
import pytest

from freezegun import freeze_time
from responses import matchers
from seriesbr import ipea

BASE_URL = "http://ipeadata2-homologa.ipea.gov.br/api/v1/ValoresSerie(SERCODIGO='BM12_TJOVER12')"


@freeze_time("2021-12-31")
@responses.activate
@pytest.mark.parametrize(
    "kwargs,expected",
    [
        (
            {},
            {
                "url": BASE_URL,
                "params": {},
            },
        ),
        (
            {"start": "2019"},
            {
                "url": BASE_URL,
                "params": {
                    "$filter": "VALDATA ge 2019-01-01T00:00:00-03:00",
                },
            },
        ),
        (
            {"start": "2019-11"},
            {
                "url": BASE_URL,
                "params": {
                    "$filter": "VALDATA ge 2019-11-01T00:00:00-03:00",
                },
            },
        ),
        (
            {"start": "2019-11-07"},
            {
                "url": BASE_URL,
                "params": {
                    "$filter": "VALDATA ge 2019-11-07T00:00:00-03:00",
                },
            },
        ),
        (
            {"end": "2019"},
            {
                "url": BASE_URL,
                "params": {
                    "$filter": "VALDATA le 2019-12-31T00:00:00-03:00",
                },
            },
        ),
        (
            {"end": "2019-11"},
            {
                "url": BASE_URL,
                "params": {
                    "$filter": "VALDATA le 2019-11-30T00:00:00-03:00",
                },
            },
        ),
        (
            {"end": "2019-11-07"},
            {
                "url": BASE_URL,
                "params": {
                    "$filter": "VALDATA le 2019-11-07T00:00:00-03:00",
                },
            },
        ),
        (
            {"start": "2019", "end": "2019"},
            {
                "url": BASE_URL,
                "params": {
                    "$filter": "VALDATA ge 2019-01-01T00:00:00-03:00 and VALDATA le 2019-12-31T00:00:00-03:00",
                },
            },
        ),
        (
            {"start": "2019-11", "end": "2019-11"},
            {
                "url": BASE_URL,
                "params": {
                    "$filter": "VALDATA ge 2019-11-01T00:00:00-03:00 and VALDATA le 2019-11-30T00:00:00-03:00",
                },
            },
        ),
        (
            {"start": "2019-11-07", "end": "2019-11-07"},
            {
                "url": BASE_URL,
                "params": {
                    "$filter": "VALDATA ge 2019-11-07T00:00:00-03:00 and VALDATA le 2019-11-07T00:00:00-03:00",
                },
            },
        ),
    ],
)
def test_ipea_get_series_url(kwargs, expected):
    expected_url = expected["url"]
    expected_params = expected["params"]

    responses.add(
        responses.GET,
        "http://ipeadata2-homologa.ipea.gov.br/api/v1/Metadados('BM12_TJOVER12')",
        json={
            "value": [
                {
                    "SERCODIGO": "BM12_TJOVER12",
                    "SERMAXDATA": "2021-12-31T00:00:00-03:00",
                    "SERMINDATA": "2019-01-01T00:00:00-03:00",
                }
            ]
        },
        status=200,
    )

    responses.add(
        responses.GET,
        expected_url,
        json={
            "value": [
                {
                    "VALDATA": "2019-01-01T00:00:00-03:00",
                    "VALVALOR": 4.41,
                }
            ],
        },
        match=[
            matchers.query_param_matcher(
                {"$select": "VALDATA,VALVALOR", **expected_params}
            )
        ],
        match_querystring=False,
        status=200,
    )

    ipea.get_series("BM12_TJOVER12", **kwargs)


@freeze_time("2021-12-31")
@responses.activate
@pytest.mark.parametrize(
    "periodicity,kwargs,expected",
    [
        (
            "Mensal",
            {"last_n": 6},
            {
                "params": {
                    "$filter": "VALDATA gt 2019-06-01T00:00:00-03:00",
                },
            },
        ),
        (
            "Trimestral",
            {"last_n": 2},
            {
                "params": {
                    "$filter": "VALDATA gt 2019-06-01T00:00:00-03:00",
                },
            },
        ),
        (
            "Anual",
            {"last_n": 1},
            {
                "params": {
                    "$filter": "VALDATA gt 2018-12-01T00:00:00-03:00",
                },
            },
        ),
        (
            "Decenal",
            "2019-12-01T00:00:00-03:00",
            {"last_n": 1},
            {
                "params": {
                    "$filter": "VALDATA gt 2009-12-01T00:00:00-03:00",
                },
            },
        ),
        (
            "Quadrienal",
            {"last_n": 1},
            {
                "params": {
                    "$filter": "VALDATA gt 2015-12-01T00:00:00-03:00",
                },
            },
        ),
        (
            "Quinquenal",
            {"last_n": 1},
            {
                "params": {
                    "$filter": "VALDATA gt 2014-12-01T00:00:00-03:00",
                },
            },
        ),
        (
            "Irregular",
            {"last_n": 1},
            {
                "params": {
                    "$filter": "VALDATA gt 2019-12-01T00:00:00-03:00",
                },
            },
        ),
        (
            "NOT_IMPLEMENTED",
            {"last_n": 1},
            {
                "params": {
                    "$filter": "VALDATA gt 2019-12-01T00:00:00-03:00",
                },
            },
        ),
    ],
)
def test_ipea_get_series_url_last_n(periodicity, kwargs, expected):
    expected_params = expected["params"]

    responses.add(
        responses.GET,
        "http://ipeadata2-homologa.ipea.gov.br/api/v1/Metadados('BM12_TJOVER12')",
        json={
            "value": [
                {
                    "SERCODIGO": "BM12_TJOVER12",
                    "SERMAXDATA": "2019-12-01T00:00:00-03:00",
                    "SERMINDATA": "2019-01-01T00:00:00-03:00",
                    "PERNOME": periodicity,
                }
            ]
        },
        status=200,
    )

    responses.add(
        responses.GET,
        BASE_URL,
        json={
            "value": [
                {
                    "VALDATA": "2019-01-01T00:00:00-03:00",
                    "VALVALOR": 4.41,
                }
            ],
        },
        match=[
            matchers.query_param_matcher(
                {"$select": "VALDATA,VALVALOR", **expected_params}
            )
        ],
        match_querystring=False,
        status=200,
    )

    ipea.get_series("BM12_TJOVER12", **kwargs)


@responses.activate
def test_ipea_get_series_dataframe():
    responses.add(
        responses.GET,
        "http://ipeadata2-homologa.ipea.gov.br/api/v1/Metadados('BM12_TJOVER12')",
        json={
            "value": [
                {
                    "SERCODIGO": "BM12_TJOVER12",
                    "SERMAXDATA": "2021-12-31T00:00:00-03:00",
                    "SERMINDATA": "2019-01-01T00:00:00-03:00",
                }
            ]
        },
        status=200,
    )

    responses.add(
        responses.GET,
        "http://ipeadata2-homologa.ipea.gov.br/api/v1/ValoresSerie(SERCODIGO='BM12_TJOVER12')",
        json={
            "value": [
                {
                    "VALDATA": "2019-01-01T00:00:00-03:00",
                    "VALVALOR": 4.41,
                }
            ],
        },
        status=200,
    )

    df = ipea.get_series({"Selic": "BM12_TJOVER12"})
    expected_df = pd.DataFrame(
        {"Selic": [4.41]}, index=pd.DatetimeIndex(["01/01/2019"], name="Date")
    )

    pd.testing.assert_frame_equal(df, expected_df)


@responses.activate
def test_ipea_get_metadata():
    responses.add(
        responses.GET,
        "http://ipeadata2-homologa.ipea.gov.br/api/v1/Metadados('BM12_TJOVER12')",
        json={
            "value": [
                {
                    "SERCODIGO": "BM12_TJOVER12",
                }
            ]
        },
        status=200,
    )

    assert ipea.get_metadata("BM12_TJOVER12") == {
        "SERCODIGO": "BM12_TJOVER12",
    }
