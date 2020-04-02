import os
import sys
import pandas
import unittest

from unittest.mock import Mock, patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import seriesbr.helpers.utils as utils  # noqa: E402


def return_first_argument(arg, **kwargs):
    return arg


class TestCat(unittest.TestCase):
    """This function concatenates every iterable with a delimiter, except for strings"""

    def test_concatenate_list(self):
        test = utils.cat([1, 2, 3, 4], ",")
        expected = "1,2,3,4"
        self.assertEqual(test, expected)

    def test_concatenate_number(self):
        test = utils.cat(2, ",")
        expected = 2
        self.assertEqual(test, expected)

    def test_concatenate_tuple(self):
        test = utils.cat((4, 5), ",")
        expected = "4,5"
        self.assertEqual(test, expected)

    def test_concatenate_string(self):
        test = utils.cat("123", ",")
        expected = "123"
        self.assertEqual(test, expected)


class TestIsIterable(unittest.TestCase):
    """This function only disregards strings as iterables"""

    def test_is_isterable_list(self):
        test = utils.is_iterable([1])
        expected = True
        self.assertEqual(test, expected)

    def test_is_isterable_tuple(self):
        test = utils.is_iterable((1,))
        expected = True
        self.assertEqual(test, expected)

    def test_is_isterable_int(self):
        test = utils.is_iterable(1)
        expected = False
        self.assertEqual(test, expected)

    def test_is_isterable_dict(self):
        test = utils.is_iterable({1: 1})
        expected = True
        self.assertEqual(test, expected)

    def test_is_isterable_str(self):
        test = utils.is_iterable("1")
        expected = False
        self.assertEqual(test, expected)


df = pandas.DataFrame(
    {"id": [1, 2], "nome": [2, 3], "pesquisa_nome": [4, 5], "pesquisa_id": [3, 4]}
)


@patch.object(pandas.DataFrame, "query")
class TestSearchDataFrame(unittest.TestCase):
    """Test wrapper around DataFrame query method"""

    def test_search_int(self, query):
        utils.search_df(df, 1)
        expected = "nome.str.contains('(?iu)1')"
        query.assert_called_with(expected, engine="python")

    def test_search_str(self, query):
        utils.search_df(df, "oi")
        expected = "nome.str.contains('(?iu)oi')"
        query.assert_called_with(expected, engine="python")

    def test_search_simple_list(self, query):
        utils.search_df(df, [1])
        expected = "nome.str.contains('(?iu)1')"
        query.assert_called_with(expected, engine="python")

    def test_search_full_list(self, query):
        utils.search_df(df, [1, 2, 3])
        expected = "nome.str.contains('(?iu)1|2|3')"
        query.assert_called_with(expected, engine="python")

    def test_search_name_and_additional_col_as_str(self, query):
        utils.search_df(df, "nome", {"pesquisa_nome": "pesquisa"})
        expected = "nome.str.contains('(?iu)nome') and pesquisa_nome.str.contains('(?iu)pesquisa')"
        query.assert_called_with(expected, engine="python")

    def test_search_name_and_additional_col_as_lists(self, query):
        utils.search_df(df, ["nome", "outro"], {"pesquisa_nome": ["pesquisa", "outra"]})
        expected = "nome.str.contains('(?iu)nome|outro') and pesquisa_nome.str.contains('(?iu)pesquisa|outra')"
        query.assert_called_with(expected, engine="python")

    def test_search_with_two_additional_cols(self, query):
        utils.search_df(
            df, ["oi", "tudo"], {"pesquisa_nome": ["DD", "DI"], "pesquisa_id": "AA"}
        )
        expected = "nome.str.contains('(?iu)oi|tudo') and pesquisa_nome.str.contains('(?iu)DD|DI') and pesquisa_id.str.contains('(?iu)AA')"
        query.assert_called_with(expected, engine="python")


class TestSearchDfErrorHandling(unittest.TestCase):
    """Test function search_df error handling"""

    def test_if_raises_do_search_invalid_filter(self):
        with self.assertRaises(ValueError):
            utils.search_df(df, "nome", {"non_existent_column": "string"})


class TestReturnCodesAndNames(unittest.TestCase):
    """
    Test function to collect arguments.

    Dictionary keys are 'names' and all other values
    are just values. This is used to help label the
    returned DataFrame with the passed arguments.
    """

    def test_collect_codes_and_names_dict(self):
        test = utils.collect_codes_and_names({"A": 1, "B": 2}, 2, 3)
        expected = ([1, 2, 2, 3], ["A", "B", 2, 3])
        self.assertTupleEqual(test, expected)

    def test_collect_codes_and_names_no_dict(self):
        test = utils.collect_codes_and_names(2, 3, 4)
        expected = ([2, 3, 4], [2, 3, 4])
        self.assertTupleEqual(test, expected)


if __name__ == "__main__":
    unittest.main(failfast=True)

# vi: nowrap
