import requests
import json

s = requests.Session()


def get_json(url, **kwargs):
    """
    Auxiliary function to make get requests
    within a HTTP Session.

    Parameters
    ----------
    url : str
        Url to be requested.

    **kwargs
        Passed to Session().get()

    Returns
    -------
    dict
        Decoded JSON.
    """
    response = s.get(url, timeout=60, **kwargs)
    response.raise_for_status()
    try:
        return response.json()
    except json.JSONDecodeError:
        raise ValueError(f"A request to {url} didn't produce any JSON.")
