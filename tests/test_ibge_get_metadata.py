import os
import sys
import unittest

from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import seriesbr.ibge as ibge  # noqa: E402
from mock_helpers import get_sample_json  # noqa: E402


class TestIbgeGetMetadata(unittest.TestCase):
    """Test if get_metadata parses JSON correctly"""

    @patch("seriesbr.helpers.metadata.get_json")
    def test_ibge_get_metadata(self, mocked_get_json):
        mocked_get_json.return_value = get_sample_json("ibge_metadata.json")

        self.assertFalse(ibge.get_metadata(1419).empty)


if __name__ == "__main__":
    unittest.main()
