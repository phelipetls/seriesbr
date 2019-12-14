import os
import sys
import json
import unittest
from unittest.mock import patch
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import seriesbr.ibge as ibge


class TestIbgeGetMetadata(unittest.TestCase):

    def setUp(self):
        json_path = Path(__file__).resolve().parent / "sample_jsons" / "ibge_metadata"
        with json_path.open() as json_file:
            self.json = json.load(json_file)

    @patch('seriesbr.ibge.get_json')
    def test_ibge_get_metadata(self, mocked_get_json):
        mocked_get_json.return_value = self.json
        self.assertFalse(ibge.get_metadata(1419).empty)


if __name__ == "__main__":
    unittest.main()
