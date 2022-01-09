import pytest
import responses
import pandas as pd

from freezegun import freeze_time
from responses import matchers
from seriesbr import bcb


BASE_URL = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados"


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
            {"last_n": 10},
            {
                "url": BASE_URL + "/ultimos/10",
                "params": {},
            },
        ),
        (
            {"start": "2019"},
            {
                "url": BASE_URL,
                "params": {"dataInicial": "01/01/2019"},
            },
        ),
        (
            {"start": "2019-11"},
            {
                "url": BASE_URL,
                "params": {"dataInicial": "01/11/2019"},
            },
        ),
        (
            {"start": "2019-11-07"},
            {
                "url": BASE_URL,
                "params": {"dataInicial": "07/11/2019"},
            },
        ),
        (
            {"end": "2019"},
            {
                "url": BASE_URL,
                "params": {"dataFinal": "31/12/2019"},
            },
        ),
        (
            {"end": "2019-11"},
            {
                "url": BASE_URL,
                "params": {"dataFinal": "30/11/2019"},
            },
        ),
        (
            {"end": "2019-11-07"},
            {
                "url": BASE_URL,
                "params": {"dataFinal": "07/11/2019"},
            },
        ),
    ],
)
def test_bcb_get_series_url(kwargs, expected):
    expected_url = expected["url"]
    expected_params = expected["params"]

    responses.add(
        responses.GET,
        expected_url,
        match=[matchers.query_param_matcher({"format": "json", **expected_params})],
        match_querystring=False,
        json=[{"data": "01/01/2019", "valor": "100"}],
        status=200,
    )

    bcb.get_series(11, **kwargs)


@responses.activate
def test_bcb_get_series_dataframe():
    responses.add(
        responses.GET,
        "https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados",
        json=[{"data": "01/01/2019", "valor": "100"}],
        status=200,
    )

    df = bcb.get_series({"Selic": 11})
    expected_df = pd.DataFrame(
        data={"Selic": [100.0]}, index=pd.DatetimeIndex(["01/01/2019"], name="Date")
    )

    pd.testing.assert_frame_equal(df, expected_df)


@responses.activate
def test_bcb_get_metadata():
    responses.add(
        responses.GET,
        "https://dadosabertos.bcb.gov.br/api/3/action/package_search?fq=codigo_sgs:11",
        json={
            "result": {
                "results": [{"code": "11"}],
            },
        },
        status=200,
    )

    assert bcb.get_metadata(11) == {"code": "11"}
