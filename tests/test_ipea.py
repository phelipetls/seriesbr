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
                "params": {
                    "$filter": "VALDATA ge 1970-01-01T00:00:00Z and VALDATA le 2021-12-31T00:00:00Z",
                },
            },
        ),
        (
            {"start": "2019"},
            {
                "url": BASE_URL,
                "params": {
                    "$filter": "VALDATA ge 2019-01-01T00:00:00Z and VALDATA le 2021-12-31T00:00:00Z",
                },
            },
        ),
        (
            {"start": "2019-11"},
            {
                "url": BASE_URL,
                "params": {
                    "$filter": "VALDATA ge 2019-11-01T00:00:00Z and VALDATA le 2021-12-31T00:00:00Z",
                },
            },
        ),
        (
            {"start": "2019-11-07"},
            {
                "url": BASE_URL,
                "params": {
                    "$filter": "VALDATA ge 2019-07-11T00:00:00Z and VALDATA le 2021-12-31T00:00:00Z",
                },
            },
        ),
        (
            {"end": "2019"},
            {
                "url": BASE_URL,
                "params": {
                    "$filter": "VALDATA ge 1970-01-01T00:00:00Z and VALDATA le 2019-12-31T00:00:00Z",
                },
            },
        ),
        (
            {"end": "2019-11"},
            {
                "url": BASE_URL,
                "params": {
                    "$filter": "VALDATA ge 1970-01-01T00:00:00Z and VALDATA le 2019-11-30T00:00:00Z",
                },
            },
        ),
        (
            {"end": "2019-11-07"},
            {
                "url": BASE_URL,
                "params": {
                    "$filter": "VALDATA ge 1970-01-01T00:00:00Z and VALDATA le 2019-07-11T00:00:00Z",
                },
            },
        ),
        (
            {"start": "2019", "end": "2019"},
            {
                "url": BASE_URL,
                "params": {
                    "$filter": "VALDATA ge 2019-01-01T00:00:00Z and VALDATA le 2019-12-31T00:00:00Z",
                },
            },
        ),
        (
            {"start": "2019-11", "end": "2019-11"},
            {
                "url": BASE_URL,
                "params": {
                    "$filter": "VALDATA ge 2019-11-01T00:00:00Z and VALDATA le 2019-11-30T00:00:00Z",
                },
            },
        ),
        (
            {"start": "2019-11-07", "end": "2019-11-07"},
            {
                "url": BASE_URL,
                "params": {
                    "$filter": "VALDATA ge 2019-07-11T00:00:00Z and VALDATA le 2019-07-11T00:00:00Z",
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
    )

    ipea.get_series("BM12_TJOVER12", **kwargs)


@responses.activate
def test_ipea_get_series_dataframe():
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
def test_get_metadata():
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

    df = ipea.get_metadata("BM12_TJOVER12")
    expected_df = pd.DataFrame({"values": "BM12_TJOVER12"}, index=["SERCODIGO"])

    pd.testing.assert_frame_equal(df, expected_df)
