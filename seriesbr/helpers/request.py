import urllib3
import json


http = urllib3.PoolManager()


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
    response = http.request("GET", url, timeout=60.0, retries=3)
    try:
        return json.loads(response.date.decode("utf-8"))
    except json.JSONDecodeError:
        raise ValueError(f"A request to {url} didn't produce any JSON.")
