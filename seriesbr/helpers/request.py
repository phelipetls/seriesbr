import functools
import requests
import json

s = requests.Session()


@functools.lru_cache(maxsize=16)
def get_json(url, **kwargs):
    """
    Wrapper around requests.Session.get().

    Parameters
    ----------
    url : str

    **kwargs
        Passed to requests.Session().get()

    Raises
    ------
    HTTPError
        In case of a HTTPError.

    ValueError
        If no JSON was returned.

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
