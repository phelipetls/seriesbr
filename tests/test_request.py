import os
import sys
import requests
import unittest
import requests_mock

from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from seriesbr.helpers import request  # noqa: E402


class TestRequest(unittest.TestCase):
    """Test function to handle API requests."""

    @requests_mock.Mocker()
    def test_get_json_raising_JSON_error(self, m):
        m.get("https://google.com", text="{invalid: json")

        with self.assertRaises(ValueError):
            request.get_json("https://google.com")

    def test_get_json_raising_HTTP_error(self):
        response = requests.Response()
        response.status_code = 404

        with patch.object(request.s, "get", return_value=response):
            with self.assertRaises(requests.HTTPError):
                request.get_json("https://google.com")


if __name__ == "__main__":
    unittest.main()
