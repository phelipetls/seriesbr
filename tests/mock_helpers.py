import json
import datetime

from pathlib import Path


def get_sample_json(filename):
    path = Path(__file__).resolve().parent / "sample_jsons" / filename
    with path.open() as f:
        return json.load(f)


def mocked_get_today_date():
    return datetime.datetime(2019, 12, 2)
