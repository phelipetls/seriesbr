import requests

s = requests.Session()


def get(url: str, **kwargs) -> requests.Response:
    response = s.get(url, timeout=60, **kwargs)
    response.raise_for_status()
    return response
