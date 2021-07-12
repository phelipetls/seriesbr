import pytest
import responses
import pandas as pd

from seriesbr import ipea


@responses.activate
def test_timeseries_json_to_dataframe():
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
def test_metadata_json_to_dataframe():
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


@responses.activate
def test_search_results_json_to_dataframe():
    responses.add(
        responses.GET,
        "http://ipeadata2-homologa.ipea.gov.br/api/v1/Metadados?$select=SERCODIGO,SERNOME,PERNOME,UNINOME&$filter=contains(SERNOME,'Selic')",
        json={
            "@odata.context": "http://ipeadata2-homologa.ipea.gov.br/api/v1/$metadata#Metadados(SERCODIGO,SERNOME,PERNOME,UNINOME)",
            "value": [
                {
                    "SERCODIGO": "BM12_TJOVER12",
                    "SERNOME": "Selic",
                    "PERNOME": "Mensal",
                    "UNINOME": "R$",
                }
            ],
        },
        status=200,
    )

    df = ipea.search("Selic")
    expected_df = pd.DataFrame(
        {
            "SERCODIGO": ["BM12_TJOVER12"],
            "SERNOME": ["Selic"],
            "PERNOME": ["Mensal"],
            "UNINOME": ["R$"],
        }
    )

    pd.testing.assert_frame_equal(df, expected_df)
