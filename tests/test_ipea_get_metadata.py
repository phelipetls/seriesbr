import os
import sys
import unittest

from unittest.mock import patch

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


if __name__ == "__main__":
    unittest.main()

# vi: nowrap
