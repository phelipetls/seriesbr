import os
import sys
import unittest

from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from seriesbr import bcb  # noqa: E402
from mock_helpers import get_json, mock_json  # noqa: E402

URL = "https://dadosabertos.bcb.gov.br/api/3/action/package_search?fq=codigo_sgs:20786"


class TestBCBGetMetadata_URL(unittest.TestCase):
    """Test if the get_metadata builds the correct url"""

    @patch("seriesbr.bcb.bcb_metadata_to_df")
    def test_url(self, mocked_bcb_metadata_to_df):
        bcb.get_metadata(20786)
        mocked_bcb_metadata_to_df.assert_called_with(URL)


class TestBCBGetMetadata(unittest.TestCase):
    """Test if get_metadata parses JSON correctly"""

    def setUp(self):
        mock_json(
            path="seriesbr.helpers.metadata.get_json",
            json=get_json("bcb_metadata.json"),
        ).start()

    def test_dataframe(self):
        test = bcb.get_metadata(20786)

        self.assertFalse(test.empty)

    def tearDown(self):
        patch.stopall()


if __name__ == "__main__":
    unittest.main()

# vi: nowrap
