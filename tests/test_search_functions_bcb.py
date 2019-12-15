import os
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from seriesbr import bcb


def mocked_search_results(url):
    return url


@patch('seriesbr.bcb.return_search_results_bcb', mocked_search_results)
class TestBCBSearch(unittest.TestCase):

    def test_search_bcb(self):
        correct = "https://dadosabertos.bcb.gov.br/api/3/action/package_search?q=spread&rows=10&start=1&sort=score desc"
        self.assertEqual(bcb.search("spread"), correct)

    def test_search_with_more_args_bcb(self):
        correct = "https://dadosabertos.bcb.gov.br/api/3/action/package_search?q=spread&rows=10&start=1&sort=score desc&fq=mensal+livre"
        self.assertEqual(bcb.search("spread", "mensal", "livre"), correct)

    def test_search_with_more_args_and_rows_bcb(self):
        correct = "https://dadosabertos.bcb.gov.br/api/3/action/package_search?q=spread&rows=30&start=5&sort=score desc&fq=mensal+livre"
        self.assertEqual(bcb.search("spread", "mensal", "livre", rows=30, start=5), correct)


if __name__ == "__main__":
    unittest.main()

# vi: nowrap
