import pytest
from seriesbr.bcb import url_builders


URL = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados?format=json"


class TestBcbSeriesUrl:
    """Test Bcb url builder to get a time series"""

    def test_invalid_type(self):
        with pytest.raises(AssertionError):
            url_builders.series.build_url({})

    def test_crazy_date(self):
        with pytest.raises(ValueError):
            url_builders.series.build_url(11, "not a date")
