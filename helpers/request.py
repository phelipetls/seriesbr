import requests


def custom_get(url, *args, **kwargs):
    response = requests.get(url, **kwargs, timeout=1000)
    response.raise_for_status()
    return response
