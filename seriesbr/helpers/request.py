import requests

s = requests.Session()


def custom_get(url, **kwargs):
    response = s.get(url, timeout=120, **kwargs)
    response.raise_for_status()
    return response
