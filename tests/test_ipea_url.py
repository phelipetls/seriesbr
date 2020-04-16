import unittest

from seriesbr.helpers import api


class TestIpeaSelect(unittest.TestCase):
    default = "?$select=SERCODIGO,SERNOME,PERNOME,UNINOME"

    def test_empty(self):
        test = api.ipea_select()
        self.assertEqual(test, self.default)

    def test_included(self):
        """Should have no effect since it's already there"""
        test = api.ipea_select(["SERCODIGO", "SERNOME"])
        self.assertEqual(test, self.default)

    def test_not_included(self):
        test = api.ipea_select(["FNTNOME"])
        expected = ",FNTNOME"
        self.assertEqual(test, self.default + expected)


class TestIpeaFilter(unittest.TestCase):
    def test_filter_name(self):
        test = api.ipea_filter("selic")
        expected = "&$filter=contains(SERNOME,'selic')"
        self.assertEqual(test, expected)

    def test_filter_multiple_names(self):
        test = api.ipea_filter(["selic", "pib"])
        expected = "&$filter=(contains(SERNOME,'selic') and contains(SERNOME,'pib'))"
        self.assertEqual(test, expected)

    def test_name_and_metadata(self):
        test = api.ipea_filter("selic", {"FNTNOME": "fonte"})
        expected = "&$filter=contains(SERNOME,'selic') and contains(FNTNOME,'fonte')"
        self.assertEqual(test, expected)

    def test_string_metadata(self):
        test = api.ipea_filter(metadata={"SERSTATUS": "A"})
        expected = "&$filter=SERSTATUS eq 'A'"
        self.assertEqual(test, expected)

    def test_numeric_metadata(self):
        test = api.ipea_filter(metadata={"SERNUMERICA": 10})
        expected = "&$filter=SERNUMERICA eq 10"
        self.assertEqual(test, expected)

    def test_name_and_multiple_metadata(self):
        test = api.ipea_filter("selic", {"PERNOME": ["mensal", "trimestral"]})
        expected = "&$filter=contains(SERNOME,'selic') and (contains(PERNOME,'mensal') or contains(PERNOME,'trimestral'))"
        self.assertEqual(test, expected)

    def test_multiple_metadata(self):
        test = api.ipea_filter(metadata={"PERNOME": ["mensal", "trimestral"]})
        expected = "&$filter=(contains(PERNOME,'mensal') or contains(PERNOME,'trimestral'))"
        self.assertEqual(test, expected)

    def test_raises_if_invalid_field(self):
        with self.assertRaises(ValueError):
            api.ipea_filter("", {"INVALID_FILTER": "INVALID"})


class TestIpeaDates(unittest.TestCase):
    def test_start(self):
        test = api.ipea_date(start="2019-01-01T00:00:00-00:00")
        expected = "&$filter=VALDATA ge 2019-01-01T00:00:00-00:00"
        self.assertEqual(test, expected)

    def test_end(self):
        test = api.ipea_date(end="2019-01-01T00:00:00-00:00")
        expected = "&$filter=VALDATA le 2019-01-01T00:00:00-00:00"
        self.assertEqual(test, expected)

    def test_start_and_end(self):
        test = api.ipea_date(
            start="2019-01-01T00:00:00-00:00", end="2019-01-01T00:00:00-00:00"
        )
        expected = "&$filter=VALDATA ge 2019-01-01T00:00:00-00:00 and VALDATA le 2019-01-01T00:00:00-00:00"
        self.assertEqual(test, expected)


if __name__ == "__main__":
    unittest.main(failfast=True)

# vi: nowrap
