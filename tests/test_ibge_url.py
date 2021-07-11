from freezegun import freeze_time

from seriesbr.ibge import build_series_url
from seriesbr.helpers.api import (
    ibge_filter_by_date,
    ibge_filter_by_classification,
    ibge_filter_by_location,
    ibge_filter_by_variable,
)


@freeze_time("2019-12-02")
class TestIbgeSeriesUrl:
    def test_with_series_code(self):
        assert build_series_url(1419) == (
            "https://servicodados.ibge.gov.br/api/v3/agregados/1419/"
            "periodos/197001-201912/variaveis?&localidades=BR&view=flat"
        )

    def test_with_location_and_classification(self):
        assert build_series_url(1419, brazil=True, classifications=2) == (
            "https://servicodados.ibge.gov.br/api/v3/agregados/1419/"
            "periodos/197001-201912/variaveis?&localidades=BR&classificacao=2[all]&view=flat"
        )


@freeze_time("2019-12-02")
class TestIbgeDates:
    def test_last_n(self):
        assert ibge_filter_by_date(last_n=5) == "/periodos/-5"

    def test_start(self):
        assert ibge_filter_by_date(start="01/2017") == "/periodos/201701-201912"

    def test_end(self):
        assert ibge_filter_by_date(end="07/2017") == "/periodos/197001-201707"

    def test_start_and_end(self):
        assert ibge_filter_by_date(start="05-2015", end="07-2017") == "/periodos/201505-201707"

    def test_start_and_end_yearly(self):
        assert ibge_filter_by_date(start="05-2015", end="07-2017", freq="anual") == (
            "/periodos/2015-2017"
        )

    def test_start_and_end_quarterly(self):
        assert ibge_filter_by_date(start="05-2015", end="07-2017", freq="trimestral") == (
            "/periodos/201502-201703"
        )


class TestIbgeVariables:
    def test_empty(self):
        assert ibge_filter_by_variable() == "/variaveis"

    def test_int(self):
        assert ibge_filter_by_variable(100) == "/variaveis/100"

    def test_str(self):
        assert ibge_filter_by_variable("100") == "/variaveis/100"

    def test_list(self):
        assert ibge_filter_by_variable([1, 2, 3]) == "/variaveis/1|2|3"


class TestIbgeLocations:
    def test_empty(self):
        assert ibge_filter_by_location() == "&localidades=BR"

    def test_dict_with_nones(self):
        assert ibge_filter_by_location(cities=None, municipalities=None) == "&localidades=BR"

    def test_brazil_non_false(self):
        assert ibge_filter_by_location(brazil="yes") == "&localidades=BR"

    def test_bool(self):
        assert ibge_filter_by_location(states=True) == "&localidades=N3"

    def test_truthy(self):
        assert ibge_filter_by_location(states="all") == "&localidades=N3"

    def test_int(self):
        assert ibge_filter_by_location(states=2) == "&localidades=N3[2]"

    def test_list(self):
        assert ibge_filter_by_location(states=[2, 3, 4]) == "&localidades=N3[2,3,4]"

    def test_multiple_args(self):
        assert (
            ibge_filter_by_location(states=[2, 3, 4], municipalities=[1, 2])
            == "&localidades=N3[2,3,4]|N6[1,2]"
        )

    def test_multiple_args_mixed_types(self):
        assert (
            ibge_filter_by_location(states=True, mesoregions=4, municipalities=[1, 2])
            == "&localidades=N3|N7[4]|N6[1,2]"
        )


class TestIbgeClassifications:
    def test_none(self):
        assert ibge_filter_by_classification(self) == ""

    def test_str(self):
        assert ibge_filter_by_classification("3") == "&classificacao=3[all]"

    def test_int(self):
        assert ibge_filter_by_classification(3) == "&classificacao=3[all]"

    def test_list(self):
        assert ibge_filter_by_classification([1, 2]) == "&classificacao=1[all]|2[all]"

    def test_dict(self):
        assert ibge_filter_by_classification({1: [2, 3]}) == "&classificacao=1[2,3]"

    def test_dict_multiple_keys(self):
        assert (
            ibge_filter_by_classification({1: [2, 3], 4: [5, 6]})
            == "&classificacao=1[2,3]|4[5,6]"
        )

    def test_empty_dict(self):
        assert ibge_filter_by_classification({1: []}) == "&classificacao=1[all]"


# vi: nowrap
