import pytest
from freezegun import freeze_time
from seriesbr.bcb import url_builders


URL = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados?format=json"


@freeze_time("2019-12-02")
class TestBcbSeriesUrl:
    """Test Bcb url builder to get a time series"""

    def test_defaults(self):
        _, params = url_builders.series.build_url(11)

        assert params == {
            "dataInicial": "01/01/1970",
            "dataFinal": "02/12/2019",
            "format": "json",
        }

    def test_start_year(self):
        _, params = url_builders.series.build_url(11, "2013")

        assert params == {
            "dataInicial": "01/01/2013",
            "dataFinal": "02/12/2019",
            "format": "json",
        }

    def test_start_year_and_month(self):
        _, params = url_builders.series.build_url(11, "07-2013")

        assert params == {
            "dataInicial": "01/07/2013",
            "dataFinal": "02/12/2019",
            "format": "json",
        }

    def test_end_year(self):
        _, params = url_builders.series.build_url(11, end="1990")

        assert params == {
            "dataInicial": "01/01/1970",
            "dataFinal": "31/12/1990",
            "format": "json",
        }

    def test_end_year_and_month(self):
        _, params = url_builders.series.build_url(11, end="06-1990")

        assert params == {
            "dataInicial": "01/01/1970",
            "dataFinal": "30/06/1990",
            "format": "json",
        }

    def test_end_complete_date(self):
        _, params = url_builders.series.build_url(11, end="05-03-2016")

        assert params == {
            "dataInicial": "01/01/1970",
            "dataFinal": "05/03/2016",
            "format": "json",
        }

    def test_start_end_year(self):
        _, params = url_builders.series.build_url(11, "2013", end="2014")

        assert params == {
            "dataInicial": "01/01/2013",
            "dataFinal": "31/12/2014",
            "format": "json",
        }

    def test_start_end_year_and_month(self):
        _, params = url_builders.series.build_url(11, "07-2013", end="09-2014")

        assert params == {
            "dataInicial": "01/07/2013",
            "dataFinal": "30/09/2014",
            "format": "json",
        }

    def test_start_end_date_complete(self):
        _, params = url_builders.series.build_url(11, "05-03-2016", end="25-10-2017")

        assert params == {
            "dataInicial": "05/03/2016",
            "dataFinal": "25/10/2017",
            "format": "json",
        }

    def test_last_n(self):
        url, params = url_builders.series.build_url(11, last_n=30)

        assert "/ultimos/30" in url
        assert params == {"format": "json"}

    def test_invalid_type(self):
        with pytest.raises(AssertionError):
            url_builders.series.build_url({})

    def test_crazy_date(self):
        with pytest.raises(ValueError):
            url_builders.series.build_url(11, "not a date")


class TestBcbMetadataUrl:
    def test_metadata_url(self):
        _, params = url_builders.metadata.build_url(20786)
        assert params == {"fq": "codigo_sgs:20786"}


class TestBcbSearchUrl:
    def test_search_bcb(self):
        _, params = url_builders.search.build_url("spread")
        assert params == {"q": "spread", "rows": 10, "start": 1, "sort": "score desc"}

    def test_search_multiple_strings(self):
        _, params = url_builders.search.build_url("spread", "mensal", "livre")
        assert params == {
            "q": "spread",
            "rows": 10,
            "start": 1,
            "sort": "score desc",
            "fq": "mensal+livre",
        }

    def test_search_with_pagination(self):
        _, params = url_builders.search.build_url(
            "spread", "mensal", "livre", rows=30, start=5
        )
        assert params == {
            "q": "spread",
            "rows": 30,
            "start": 5,
            "sort": "score desc",
            "fq": "mensal+livre",
        }
