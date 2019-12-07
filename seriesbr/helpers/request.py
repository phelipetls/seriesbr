import requests
import json

s = requests.Session()


def get_json(url, **kwargs):
    response = s.get(url, timeout=120, **kwargs)
    response.raise_for_status()
    try:
        return response.json()
    except json.JSONDecodeError:
        raise ValueError(f"A request to {url} didn't produce any JSON.")
