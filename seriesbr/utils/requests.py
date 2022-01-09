import requests

s = requests.Session()


def get(url, **kwargs):
    response = s.get(url, timeout=60, **kwargs)
    response.raise_for_status()
    return response
