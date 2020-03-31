import json

from pathlib import Path
from unittest.mock import patch


def get_sample_json(filename):
    path = Path(__file__).resolve().parent / "sample_jsons" / filename
    with path.open() as f:
        return json.load(f)


def mock_json(path, json):
    return patch(path, return_value=json)
