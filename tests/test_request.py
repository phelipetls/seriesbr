import requests
import pytest

from seriesbr.helpers import request


def test_get_json_raising_JSON_error(requests_mock):
    requests_mock.get("https://google.com", text="{invalid: json")

    with pytest.raises(ValueError):
        request.get_json("https://google.com")


def test_get_json_raising_HTTP_error(requests_mock):
    requests_mock.get("https://google.com", status_code=400)

    with pytest.raises(requests.HTTPError):
        request.get_json("https://google.com")
