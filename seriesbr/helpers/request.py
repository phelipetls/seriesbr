import requests


def custom_get(url, **kwargs):
    response = requests.get(url, timeout=120, **kwargs)
    response.raise_for_status()
    return response
