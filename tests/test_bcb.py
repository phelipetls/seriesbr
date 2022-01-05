import responses
import pandas as pd

from seriesbr import bcb


@responses.activate
def test_get_series():
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
def test_get_metadata():
    responses.add(
        responses.GET,
        "https://dadosabertos.bcb.gov.br/api/3/action/package_search?fq=codigo_sgs:20786",
        json={
            "result": {
                "results": [{"code": "20786"}],
            },
        },
        status=200,
    )

    df = bcb.get_metadata(20786)
    expected_df = pd.DataFrame({"values": ["20786"]}, index=pd.Series(["code"]))

    pd.testing.assert_frame_equal(df, expected_df)
