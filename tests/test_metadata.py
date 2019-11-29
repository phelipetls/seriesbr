import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from seriesbr.helpers import metadata


class TestMetadata(unittest.TestCase):

    def test_if_right_select(self):
        select_one = metadata.ipea_make_select_query(["FNTURL"])
        select_two = metadata.ipea_make_select_query(["FNTURL", "MULNOME"])
        select_three = metadata.ipea_make_select_query(["FNTURL", "MULNOME", "SERATUALIZACAO"])
        defaults = metadata.ipea_make_select_query(["SERCODIGO", "SERNOME", "PERNOME", "UNINOME"])
        select_by_default = "?$select=SERCODIGO,SERNOME,PERNOME,UNINOME"

        self.assertEqual(select_one, select_by_default + ",FNTURL")
        self.assertEqual(select_two, select_by_default + ",FNTURL,MULNOME")
        self.assertEqual(select_three, select_by_default + ",FNTURL,MULNOME,SERATUALIZACAO")
        self.assertEqual(defaults, select_by_default)

    def test_if_right_filter(self):
        filter_one = metadata.ipea_make_filter_query('', {"FNTURL": ""})
        filter_two = metadata.ipea_make_filter_query('', {"FNTURL": "", "MULNOME": ""})
        filter_three = metadata.ipea_make_filter_query('', {"FNTURL": '', "MULNOME": '', "SERATUALIZACAO": ''})
        filter_by_default = "&$filter=contains(SERNOME,'')"

        self.assertEqual(filter_one, filter_by_default + " and contains(FNTURL,'')")
        self.assertEqual(filter_two, filter_by_default + " and contains(FNTURL,'') and contains(MULNOME,'')")
        self.assertEqual(filter_three, filter_by_default + " and contains(FNTURL,'') and contains(MULNOME,'') and contains(SERATUALIZACAO,'')")

    def test_if_invalid_field_raises_value_error(self):
        with self.assertRaises(ValueError):
            metadata.ipea_make_filter_query('', {"unidade": "percentual"})


if __name__ == "__main__":
    unittest.main()
