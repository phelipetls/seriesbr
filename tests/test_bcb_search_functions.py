import os
import sys
import json
import unittest

from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from seriesbr import bcb
from seriesbr.helpers.searching import bcb_get_search_results


def mocked_search_results(url):
    return url


def get_sample_json(filename):
    json_path = Path(__file__).resolve().parent / "sample_jsons" / filename
    with json_path.open() as json_file:
        return json.load(json_file)


@patch('seriesbr.bcb.bcb_get_search_results', mocked_search_results)
class TestBCBSearch(unittest.TestCase):

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

    @patch('seriesbr.helpers.searching.get_json')
    def test_bcb_get_search_results(self, mocked_get_json):
        mocked_get_json.return_value = get_sample_json("bcb_search_results")
        df = bcb_get_search_results(None)

        test = df.columns.tolist()
        correct = ["codigo_sgs", "title", "periodicidade", "unidade_medida"]
        self.assertListEqual(test, correct)


if __name__ == "__main__":
    unittest.main()

# vi: nowrap
