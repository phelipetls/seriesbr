import pytest

from seriesbr.helpers import api

class TestIpeaSelect:
    def test_select_default(self):
        assert api.ipea_select() == "?$select=SERCODIGO,SERNOME,PERNOME,UNINOME"


    def test_select_included_in_default(self):
        assert api.ipea_select(["SERCODIGO", "SERNOME"]) == "?$select=SERCODIGO,SERNOME,PERNOME,UNINOME"


    def test_select_not_included_in_default(self):
        assert api.ipea_select(["FNTNOME"]) == "?$select=SERCODIGO,SERNOME,PERNOME,UNINOME,FNTNOME"


class TestIpeaFilter:
    def test_filter_name(self):
        assert api.ipea_filter("selic") == "&$filter=contains(SERNOME,'selic')"


    def test_filter_multiple_names(self):
        assert api.ipea_filter(["selic", "pib"]) == (
            "&$filter=(contains(SERNOME,'selic') and contains(SERNOME,'pib'))"
        )


    def test_name_and_metadata(self):
        assert api.ipea_filter("selic", {"FNTNOME": "fonte"}) == (
            "&$filter=contains(SERNOME,'selic') and contains(FNTNOME,'fonte')"
        )


    def test_string_metadata(self):
        assert api.ipea_filter(metadata={"SERSTATUS": "A"}) == "&$filter=SERSTATUS eq 'A'"


    def test_numeric_metadata(self):
        assert api.ipea_filter(metadata={"SERNUMERICA": 10}) == "&$filter=SERNUMERICA eq 10"


    def test_name_and_multiple_metadata(self):
        assert api.ipea_filter("selic", {"PERNOME": ["mensal", "trimestral"]}) == (
            "&$filter=contains(SERNOME,'selic')"
            " and (contains(PERNOME,'mensal')"
            " or contains(PERNOME,'trimestral'))"
        )


    def test_multiple_metadata(self):
        assert api.ipea_filter(metadata={"PERNOME": ["mensal", "trimestral"]}) == (
            "&$filter=(contains(PERNOME,'mensal') or contains(PERNOME,'trimestral'))"
        )


    def test_if_invalid_field_raises_error(self):
        with pytest.raises(ValueError):
            api.ipea_filter("", {"INVALID_FILTER": "INVALID"})


class TestIpeaFilterByDate:
    def test_start(self):
        assert api.ipea_filter_by_date(start="2019-01-01") == (
            "&$filter=VALDATA ge 2019-01-01"
        )


    def test_end(self):
        assert api.ipea_filter_by_date(end="2019-01-30") == (
            "&$filter=VALDATA le 2019-01-30"
        )


    def test_start_and_end(self):
        assert api.ipea_filter_by_date(
            start="2019-01-01", end="2019-01-30"
        ) == (
            "&$filter=VALDATA ge 2019-01-01 and VALDATA le 2019-01-30"
        )
