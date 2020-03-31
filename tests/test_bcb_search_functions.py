import os
import sys
import unittest

from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from seriesbr import bcb  # noqa: E402
from mock_helpers import get_sample_json  # noqa: E402
from seriesbr.bcb import bcb_get_search_results  # noqa: E402


def mocked_search_results(url):
    return url


@patch("seriesbr.bcb.bcb_get_search_results", mocked_search_results)
class TestBCBSearchURL(unittest.TestCase):
    """Test if BCB search functions build correct URL"""

    def test_search_bcb(self):
        test = bcb.search("spread")
        correct = "https://dadosabertos.bcb.gov.br/api/3/action/package_search?q=spread&rows=10&start=1&sort=score desc"
        self.assertEqual(test, correct)

    def test_search_with_more_args_bcb(self):
        test = bcb.search("spread", "mensal", "livre")
        correct = "https://dadosabertos.bcb.gov.br/api/3/action/package_search?q=spread&rows=10&start=1&sort=score desc&fq=mensal+livre"
        self.assertEqual(test, correct)

    def test_search_with_more_args_and_rows_bcb(self):
        test = bcb.search("spread", "mensal", "livre", rows=30, start=5)
        correct = "https://dadosabertos.bcb.gov.br/api/3/action/package_search?q=spread&rows=30&start=5&sort=score desc&fq=mensal+livre"
        self.assertEqual(test, correct)


class TestBCBSearchDataFrame(unittest.TestCase):
    """Test if BCB search parses search result correctly."""

    @patch("seriesbr.helpers.searching.get_json")
    def test_bcb_get_search_results(self, mocked_get_json):
        mocked_get_json.return_value = get_sample_json("bcb_search_results.json")

        df = bcb_get_search_results("https://fake.com?json=call")

        test = df.columns.tolist()
        correct = ["codigo_sgs", "title", "periodicidade", "unidade_medida"]

        self.assertListEqual(test, correct)


if __name__ == "__main__":
    unittest.main()

# vi: nowrap
