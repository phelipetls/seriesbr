import os
import sys
import unittest

from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from seriesbr import ipea  # noqa: E402
from mock_helpers import get_json  # noqa: E402


class IPEAListFunctionsTest(unittest.TestCase):
    @patch("seriesbr.helpers.lists.get_json")
    def test_list_themes(self, mocked_get_json):
        mocked_get_json.return_value = get_json("ipea_temas.json")

        test = ipea.list_themes().columns.tolist()
        correct = ["TEMCODIGO", "TEMCODIGO_PAI", "TEMNOME"]
        self.assertListEqual(test, correct)

    @patch("seriesbr.helpers.lists.get_json")
    def test_list_countries(self, mocked_get_json):
        mocked_get_json.return_value = get_json("ipea_paises.json")

        test = ipea.list_countries().columns.tolist()
        correct = ["PAICODIGO", "PAINOME"]
        self.assertListEqual(test, correct)

    def test_list_metadata(self):
        df = ipea.list_metadata()
        self.assertFalse(df.empty)


if __name__ == "__main__":
    unittest.main()

# vi: nowrap
