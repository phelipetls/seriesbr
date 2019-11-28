import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from seriesbr.helpers import metadata


class TestMetadata(unittest.TestCase):

    select_one = metadata.ipea_make_select_query(["FNTURL"])
    select_two = metadata.ipea_make_select_query(["FNTURL", "MULNOME"])
    select_three = metadata.ipea_make_select_query(["FNTURL", "MULNOME", "SERATUALIZACAO"])
    defaults = metadata.ipea_make_select_query(["SERCODIGO", "SERNOME", "PERNOME", "UNINOME"])
    select_by_default = "?$select=SERCODIGO,SERNOME,PERNOME,UNINOME"

    filter_one = metadata.ipea_make_filter_query('', {"FNTURL": ""})
    filter_two = metadata.ipea_make_filter_query('', {"FNTURL": "", "MULNOME": ""})
    filter_three = metadata.ipea_make_filter_query('', {"FNTURL": '', "MULNOME": '', "SERATUALIZACAO": ''})
    filter_by_default = "&$filter=contains(SERNOME,'')"

    def test_if_right_select(self):
        self.assertEqual(self.select_one, self.select_by_default + ",FNTURL")
        self.assertEqual(self.select_two, self.select_by_default + ",FNTURL,MULNOME")
        self.assertEqual(self.select_three, self.select_by_default + ",FNTURL,MULNOME,SERATUALIZACAO")
        self.assertEqual(self.defaults, self.select_by_default)

    def test_if_right_filter(self):
        self.assertEqual(self.filter_one, self.filter_by_default + " and contains(FNTURL,'')")
        self.assertEqual(self.filter_two, self.filter_by_default + " and contains(FNTURL,'') and contains(MULNOME,'')")
        self.assertEqual(self.filter_three, self.filter_by_default + " and contains(FNTURL,'') and contains(MULNOME,'') and contains(SERATUALIZACAO,'')")

    def test_if_invalid_field_raises_value_error(self):
        with self.assertRaises(ValueError): metadata.ipea_make_filter_query('', {"unidade": "percentual"})


if __name__ == "__main__":
    unittest.main()
