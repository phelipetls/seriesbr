import os
import sys
import unittest

from unittest.mock import patch
from mock_helpers import get_json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from seriesbr import ipea  # noqa: E402


def mocked_metadata_to_df(url):
    return url


class TestIPEAMetadata(unittest.TestCase):
    """Test metadata function"""

    @patch("seriesbr.ipea.ipea_metadata_to_df", mocked_metadata_to_df)
    def test_get_metadata(self):
        self.assertEqual(
            ipea.get_metadata("BM12_CRLIN12"),
            "http://ipeadata2-homologa.ipea.gov.br/api/v1/Metadados('BM12_CRLIN12')",
        )


class TestIpeaMetadataToDataFrame(unittest.TestCase):
    @patch("seriesbr.helpers.metadata.get_json")
    def test_ipea_metadata_to_df(self, mocked_get_json):
        mocked_get_json.return_value = get_json("ipea_metadata.json")

        df = ipea.ipea_metadata_to_df("url")
        self.assertFalse(df.empty)


if __name__ == "__main__":
    unittest.main()

# vi: nowrap
