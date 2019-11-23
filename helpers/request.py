import requests


def get_serie(url):
    response = requests.get(url, timeout=1000)
    response.raise_for_status()
    return response.text
