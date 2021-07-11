import pytest
from freezegun import freeze_time

from seriesbr import bcb


URL = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados?format=json"


@freeze_time("2019-12-02")
class TestBcbSeriesUrl:
    """Test Bcb url builder to get a time series"""

    def test_defaults(self):
        url = bcb.build_url(11)

        assert url == f"{URL}&dataInicial=01/01/1970&dataFinal=02/12/2019"

    def test_start_year(self):
        url = bcb.build_url(11, "2013")

        assert url == f"{URL}&dataInicial=01/01/2013&dataFinal=02/12/2019"

    def test_start_year_and_month(self):
        url = bcb.build_url(11, "07-2013")

        assert url == f"{URL}&dataInicial=01/07/2013&dataFinal=02/12/2019"

    def test_end_year(self):
        url = bcb.build_url(11, end="1990")

        assert url == f"{URL}&dataInicial=01/01/1970&dataFinal=31/12/1990"

    def test_end_year_and_month(self):
        url = bcb.build_url(11, end="06-1990")

        assert url == f"{URL}&dataInicial=01/01/1970&dataFinal=30/06/1990"

    def test_end_complete_date(self):
        url = bcb.build_url(11, end="05-03-2016")

        assert url == f"{URL}&dataInicial=01/01/1970&dataFinal=05/03/2016"

    def test_start_end_year(self):
        url = bcb.build_url(11, "2013", end="2014")

        assert url == f"{URL}&dataInicial=01/01/2013&dataFinal=31/12/2014"

    def test_start_end_year_and_month(self):
        url = bcb.build_url(11, "07-2013", end="09-2014")

        assert url == f"{URL}&dataInicial=01/07/2013&dataFinal=30/09/2014"

    def test_start_end_date_complete(self):
        url = bcb.build_url(11, "05-03-2016", end="25-10-2017")

        assert url == f"{URL}&dataInicial=05/03/2016&dataFinal=25/10/2017"

    def test_last_n(self):
        url = bcb.build_url(11, last_n=30)

        assert (
            url
            == "https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados/ultimos/30?format=json"
        )

    def test_invalid_type(self):
        with pytest.raises(AssertionError):
            bcb.build_url({})

    def test_crazy_date(self):
        with pytest.raises(ValueError):
            bcb.build_url(11, "not a date")


class TestBcbMetadataUrl:
    def test_metadata_url(self):
        assert bcb.build_metadata_url(20786) == (
            "https://dadosabertos.bcb.gov.br/api/3/action/"
            "package_search?fq=codigo_sgs:20786"
        )


class TestBcbSearchUrl:
    def test_search_bcb(self):
        assert bcb.build_search_url("spread") == (
            "https://dadosabertos.bcb.gov.br/api/3/action/package_search?"
            "q=spread&rows=10&start=1&sort=score desc"
        )

    def test_search_multiple_strings(self):
        assert bcb.build_search_url("spread", "mensal", "livre") == (
            "https://dadosabertos.bcb.gov.br/api/3/action/package_search?"
            "q=spread&rows=10&start=1&sort=score desc&fq=mensal+livre"
        )

    def test_search_with_pagination(self):
        assert bcb.build_search_url("spread", "mensal", "livre", rows=30, start=5) == (
            "https://dadosabertos.bcb.gov.br/api/3/action/package_search?"
            "q=spread&rows=30&start=5&sort=score desc&fq=mensal+livre"
        )
