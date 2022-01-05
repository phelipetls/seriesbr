from seriesbr.ipea.url_builders.series import ipea_filter_by_date


class TestIpeaFilterByDate:
    def test_start(self):
        assert ipea_filter_by_date(start="2019-01-01") == ("VALDATA ge 2019-01-01")

    def test_end(self):
        assert ipea_filter_by_date(end="2019-01-30") == ("VALDATA le 2019-01-30")

    def test_start_and_end(self):
        assert ipea_filter_by_date(start="2019-01-01", end="2019-01-30") == (
            "VALDATA ge 2019-01-01 and VALDATA le 2019-01-30"
        )
