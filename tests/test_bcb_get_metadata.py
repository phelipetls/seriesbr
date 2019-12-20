import os
import sys
import unittest
import json

from unittest.mock import patch
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from seriesbr import bcb


def mocked_metadata_to_df(url):
    return url


def mocked_get_json(url):
    json_path = Path(__file__).resolve().parent / "sample_jsons" / "bcb_metadata"
    with json_path.open() as json_file:
        return json.load(json_file)


class TestBCBGetMetadata(unittest.TestCase):

    @patch('seriesbr.bcb.bcb_metadata_to_df', mocked_metadata_to_df)
    def test_if_get_metadata_returns_correct_url(self):
        test = bcb.get_metadata(20786)
        correct = "https://dadosabertos.bcb.gov.br/api/3/action/package_search?fq=codigo_sgs:20786"
        self.assertEqual(test, correct)

    @patch('seriesbr.helpers.metadata.get_json', mocked_get_json)
    def test_if_get_metadata_json_gets_parsed_correctly(self):
        test = bcb.get_metadata(20786)
        self.assertFalse(test.empty)


if __name__ == "__main__":
    unittest.main()

# vi: nowrap
