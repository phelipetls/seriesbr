import os
import sys
import unittest
import pandas
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import seriesbr.helpers.utils as utils


def return_first_argument(arg, **kwargs):
    return arg


class TestUtils(unittest.TestCase):
    def test_concatenate_by_separator_if_iterable(self):
        test = [
            utils.cat([1, 2, 3, 4], ","),
            utils.cat(2, ","),
            utils.cat((4, 5), ","),
            utils.cat("123", ","),
        ]
        correct = ["1,2,3,4", 2, "4,5", "123"]
        self.assertListEqual(test, correct)

    def test_is_isterable(self):
        to_test = [[1], (1,), 1, {1: 1}, "1"]
        test = list(map(utils.isiterable, to_test))
        correct = [True, True, False, True, False]
        self.assertListEqual(test, correct)

    @patch.object(pandas.DataFrame, "query")
    def test_do_search(self, mocked_query):
        mocked_query.side_effect = return_first_argument
        df = pandas.DataFrame({"id": [1, 2], "nome": [2, 3], "pesquisa_nome": [4, 5], "pesquisa_id": [3, 4]})
        test = [
            utils.do_search(df, "oi", {"pesquisa_nome": "DD"}),
            utils.do_search(df, ["oi", "tudo"], {"pesquisa_nome": ["DD", "DI"]}),
            utils.do_search(df, ["oi", "tudo"], {"pesquisa_nome": ["DD", "DI"], "pesquisa_id": "AA"}),
            utils.do_search(df, [1], {"pesquisa_nome": [2]}),
            utils.do_search(df, [1, 2, 3], {"pesquisa_nome": ["A", "B", "C"]}),
        ]
        correct = [
            "nome.str.contains('(?iu)oi') and pesquisa_nome.str.contains('(?iu)DD')",
            "nome.str.contains('(?iu)oi|tudo') and pesquisa_nome.str.contains('(?iu)DD|DI')",
            "nome.str.contains('(?iu)oi|tudo') and pesquisa_nome.str.contains('(?iu)DD|DI') and pesquisa_id.str.contains('(?iu)AA')",
            "nome.str.contains('(?iu)1') and pesquisa_nome.str.contains('(?iu)2')",
            "nome.str.contains('(?iu)1|2|3') and pesquisa_nome.str.contains('(?iu)A|B|C')",
        ]
        self.assertListEqual(test, correct)

    def test_if_raises_do_search_invalid_filter(self):
        df = pandas.DataFrame({"id": [1, 2], "nome": [2, 3], "pesquisa_nome": [4, 5], "pesquisa_id": [3, 4]})
        with self.assertRaises(ValueError):
            utils.do_search(df, "oi", {"non_existent_col": "a"})

    def test_return_codes_and_names_dict(self):
        test = [list(x) for x in utils.return_codes_and_names({"A": 1, "B": 2}, 2, 3)]
        correct = [[1, 2, 2, 3], ["A", "B", 2, 3]]
        self.assertListEqual(test, correct)

    def test_return_codes_and_names_no_dict(self):
        test = [list(x) for x in utils.return_codes_and_names(2, 3, 4)]
        correct = [[2, 3, 4], [2, 3, 4]]
        self.assertListEqual(test, correct)


if __name__ == "__main__":
    unittest.main(failfast=True)

# vi: nowrap
