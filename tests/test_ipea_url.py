import pytest

from seriesbr.ipea.url_builders.search import ipea_select, ipea_filter
from seriesbr.ipea.url_builders.series import ipea_filter_by_date

class TestIpeaSelect:
    def test_select_default(self):
        assert ipea_select() == "SERCODIGO,SERNOME,PERNOME,UNINOME"


    def test_select_included_in_default(self):
        assert ipea_select(["SERCODIGO", "SERNOME"]) == "SERCODIGO,SERNOME,PERNOME,UNINOME"


    def test_select_not_included_in_default(self):
        assert ipea_select(["FNTNOME"]) == "SERCODIGO,SERNOME,PERNOME,UNINOME,FNTNOME"


class TestIpeaFilter:
    def test_filter_name(self):
        assert ipea_filter("selic") == "contains(SERNOME,'selic')"


    def test_filter_multiple_names(self):
        assert ipea_filter(["selic", "pib"]) == (
            "(contains(SERNOME,'selic') and contains(SERNOME,'pib'))"
        )


    def test_name_and_metadata(self):
        assert ipea_filter("selic", {"FNTNOME": "fonte"}) == (
            "contains(SERNOME,'selic') and contains(FNTNOME,'fonte')"
        )


    def test_string_metadata(self):
        assert ipea_filter(metadata={"SERSTATUS": "A"}) == "SERSTATUS eq 'A'"


    def test_numeric_metadata(self):
        assert ipea_filter(metadata={"SERNUMERICA": 10}) == "SERNUMERICA eq 10"


    def test_name_and_multiple_metadata(self):
        assert ipea_filter("selic", {"PERNOME": ["mensal", "trimestral"]}) == (
            "contains(SERNOME,'selic')"
            " and (contains(PERNOME,'mensal')"
            " or contains(PERNOME,'trimestral'))"
        )


    def test_multiple_metadata(self):
        assert ipea_filter(metadata={"PERNOME": ["mensal", "trimestral"]}) == (
            "(contains(PERNOME,'mensal') or contains(PERNOME,'trimestral'))"
        )


    def test_if_invalid_field_raises_error(self):
        with pytest.raises(ValueError):
            ipea_filter("", {"INVALID_FILTER": "INVALID"})


class TestIpeaFilterByDate:
    def test_start(self):
        assert ipea_filter_by_date(start="2019-01-01") == (
            "VALDATA ge 2019-01-01"
        )


    def test_end(self):
        assert ipea_filter_by_date(end="2019-01-30") == (
            "VALDATA le 2019-01-30"
        )


    def test_start_and_end(self):
        assert ipea_filter_by_date(
            start="2019-01-01", end="2019-01-30"
        ) == (
            "VALDATA ge 2019-01-01 and VALDATA le 2019-01-30"
        )
