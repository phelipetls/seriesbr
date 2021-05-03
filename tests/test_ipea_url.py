import pytest

from seriesbr.helpers import api

default = "?$select=SERCODIGO,SERNOME,PERNOME,UNINOME"


def test_select_default():
    assert api.ipea_select() == default


def test_select_included_in_default():
    assert api.ipea_select(["SERCODIGO", "SERNOME"]) == default


def test_select_not_included_in_default():
    assert api.ipea_select(["FNTNOME"]) == default + ",FNTNOME"


def test_filter_name():
    assert api.ipea_filter("selic") == "&$filter=contains(SERNOME,'selic')"


def test_filter_multiple_names():
    assert api.ipea_filter(["selic", "pib"]) == (
        "&$filter=(contains(SERNOME,'selic') and contains(SERNOME,'pib'))"
    )


def test_name_and_metadata():
    assert api.ipea_filter("selic", {"FNTNOME": "fonte"}) == (
        "&$filter=contains(SERNOME,'selic') and contains(FNTNOME,'fonte')"
    )


def test_string_metadata():
    assert api.ipea_filter(metadata={"SERSTATUS": "A"}) == "&$filter=SERSTATUS eq 'A'"


def test_numeric_metadata():
    assert api.ipea_filter(metadata={"SERNUMERICA": 10}) == "&$filter=SERNUMERICA eq 10"


def test_name_and_multiple_metadata():
    assert api.ipea_filter("selic", {"PERNOME": ["mensal", "trimestral"]}) == (
        "&$filter=contains(SERNOME,'selic')"
        " and (contains(PERNOME,'mensal')"
        " or contains(PERNOME,'trimestral'))"
    )


def test_multiple_metadata():
    assert api.ipea_filter(metadata={"PERNOME": ["mensal", "trimestral"]}) == (
        "&$filter=(contains(PERNOME,'mensal') or contains(PERNOME,'trimestral'))"
    )


def test_raises_if_invalid_field():
    with pytest.raises(ValueError):
        api.ipea_filter("", {"INVALID_FILTER": "INVALID"})


def test_start():
    assert api.ipea_date(start="2019-01-01T00:00:00-00:00") == (
        "&$filter=VALDATA ge 2019-01-01T00:00:00-00:00"
    )


def test_end():
    assert api.ipea_date(end="2019-01-30T00:00:00-00:00") == (
        "&$filter=VALDATA le 2019-01-30T00:00:00-00:00"
    )


def test_start_and_end():
    assert api.ipea_date(
        start="2019-01-01T00:00:00-00:00", end="2019-01-30T00:00:00-00:00"
    ) == (
        "&$filter=VALDATA ge 2019-01-01T00:00:00-00:00 and VALDATA le 2019-01-30T00:00:00-00:00"
    )
