import pytest
from freezegun import freeze_time
from seriesbr.bcb import url_builders


URL = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados?format=json"


@freeze_time("2019-12-02")
class TestBcbSeriesUrl:
    """Test Bcb url builder to get a time series"""

    def test_defaults(self):
        url = url_builders.series.build_url(11)

        assert url == f"{URL}&dataInicial=01/01/1970&dataFinal=02/12/2019"

    def test_start_year(self):
        url = url_builders.series.build_url(11, "2013")

        assert url == f"{URL}&dataInicial=01/01/2013&dataFinal=02/12/2019"

    def test_start_year_and_month(self):
        url = url_builders.series.build_url(11, "07-2013")

        assert url == f"{URL}&dataInicial=01/07/2013&dataFinal=02/12/2019"

    def test_end_year(self):
        url = url_builders.series.build_url(11, end="1990")

        assert url == f"{URL}&dataInicial=01/01/1970&dataFinal=31/12/1990"

    def test_end_year_and_month(self):
        url = url_builders.series.build_url(11, end="06-1990")

        assert url == f"{URL}&dataInicial=01/01/1970&dataFinal=30/06/1990"

    def test_end_complete_date(self):
        url = url_builders.series.build_url(11, end="05-03-2016")

        assert url == f"{URL}&dataInicial=01/01/1970&dataFinal=05/03/2016"

    def test_start_end_year(self):
        url = url_builders.series.build_url(11, "2013", end="2014")

        assert url == f"{URL}&dataInicial=01/01/2013&dataFinal=31/12/2014"

    def test_start_end_year_and_month(self):
        url = url_builders.series.build_url(11, "07-2013", end="09-2014")

        assert url == f"{URL}&dataInicial=01/07/2013&dataFinal=30/09/2014"

    def test_start_end_date_complete(self):
        url = url_builders.series.build_url(11, "05-03-2016", end="25-10-2017")

        assert url == f"{URL}&dataInicial=05/03/2016&dataFinal=25/10/2017"

    def test_last_n(self):
        url = url_builders.series.build_url(11, last_n=30)

        assert (
            url
            == "https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados/ultimos/30?format=json"
        )

    def test_invalid_type(self):
        with pytest.raises(AssertionError):
            url_builders.series.build_url({})

    def test_crazy_date(self):
        with pytest.raises(ValueError):
            url_builders.series.build_url(11, "not a date")


class TestBcbMetadataUrl:
    def test_metadata_url(self):
        assert url_builders.metadata.build_url(20786) == (
            "https://dadosabertos.bcb.gov.br/api/3/action/"
            "package_search?fq=codigo_sgs:20786"
        )


class TestBcbSearchUrl:
    def test_search_bcb(self):
        assert url_builders.search.build_url("spread") == (
            "https://dadosabertos.bcb.gov.br/api/3/action/package_search?"
            "q=spread&rows=10&start=1&sort=score desc"
        )

    def test_search_multiple_strings(self):
        assert url_builders.search.build_url("spread", "mensal", "livre") == (
            "https://dadosabertos.bcb.gov.br/api/3/action/package_search?"
            "q=spread&rows=10&start=1&sort=score desc&fq=mensal+livre"
        )

    def test_search_with_pagination(self):
        assert url_builders.search.build_url("spread", "mensal", "livre", rows=30, start=5) == (
            "https://dadosabertos.bcb.gov.br/api/3/action/package_search?"
            "q=spread&rows=30&start=5&sort=score desc&fq=mensal+livre"
        )
