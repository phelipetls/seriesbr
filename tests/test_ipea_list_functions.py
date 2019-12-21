import os
import sys
import json
import unittest

from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from seriesbr import ipea


def get_sample_json(filename):
    json_path = Path(__file__).resolve().parent / "sample_jsons" / filename
    with json_path.open() as json_file:
        return json.load(json_file)


class IPEAListFunctionsTest(unittest.TestCase):

    @patch('seriesbr.helpers.lists.get_json')
    def test_list_themes(self, mocked_get_json):
        mocked_get_json.return_value = get_sample_json("ipea_temas")
        test = ipea.list_themes().columns.tolist()
        correct = ["TEMCODIGO", "TEMCODIGO_PAI", "TEMNOME"]
        self.assertListEqual(test, correct)

    @patch('seriesbr.helpers.lists.get_json')
    def test_list_countries(self, mocked_get_json):
        mocked_get_json.return_value = get_sample_json("ipea_paises")
        test = ipea.list_countries().columns.tolist()
        correct = ["PAICODIGO", "PAINOME"]
        self.assertListEqual(test, correct)

    def test_list_metadata(self):
        df = ipea.list_metadata()
        self.assertFalse(df.empty)


if __name__ == "__main__":
    unittest.main()

# vi: nowrap
