import pytest
import pandas as pd

from seriesbr import seriesbr
from fixture_utils import read_json

BCB = read_json("bcb_json.json")
IPEA = read_json("ipea_json.json")


@pytest.fixture
def setup(mocker):
    mocker.patch("seriesbr.helpers.timeseries.get_json", side_effect=[IPEA, BCB])


def test_dataframe(setup):
    df = seriesbr.get_series({"Inadimplência": "BM12_CRLIN12", "Spread": 20786})

    assert not df.empty
    assert df.columns.tolist() == ["Inadimplência", "Spread"]
    assert pd.api.types.is_numeric_dtype(df.values)
    assert pd.api.types.is_datetime64_any_dtype(df.index)
