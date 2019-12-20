from pandas import DataFrame
from .request import get_json


def bcb_metadata_to_df(url):
    """
    Auxiliary function to request metadata
    from BCB database and turn the returned
    JSON into a DataFrame.

    Parameters
    ----------
    url : str
        Url to be requested.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with metadatas in its columns.
    """
    json = get_json(url)["result"]["results"][0]
    return DataFrame.from_dict(json, orient="index", columns=["values"])


def ipea_metadata_to_df(url):
    """
    Auxiliary function to request metadata
    from IPEA database and turn the returned
    JSON into a DataFrame.

    Parameters
    ----------
    url : str
        Url to be requested.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with metadatas in its columns.
    """
    json = get_json(url)["value"][0]
    return DataFrame.from_dict(json, orient="index", columns=["values"])


def ibge_metadata_to_df(url):
    """
    Auxiliary function to request metadata
    from IBGE database and turn the returned
    JSON into a DataFrame.

    Parameters
    ----------
    url : str
        Url to be requested.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with metadatas in its columns.
    """
    json = get_json(url)
    return DataFrame.from_dict(json, orient="index", columns=["values"])
