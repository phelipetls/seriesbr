from pandas import DataFrame
from .request import get_json

metadata_list = ["codigo_sgs", "title", "periodicidade", "unidade_medida"]


def bcb_get_search_results(url):
    """
    Auxiliary function to request BCB's search
    results and turn json into a DataFrame.

    Parameters
    ----------
    url : str
        Url to be requested.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with the search results.

    Raises
    ------
    AssertionError
        If nothing was found.
    """
    json = get_json(url)
    search_results = json["result"]["results"]
    assert search_results, "Nothing was found."
    return DataFrame(search_results).loc[:, metadata_list]


def ipea_get_search_results(url):
    """
    Auxiliary function to request IPEA's search
    results and turn json into a DataFrame.

    Parameters
    ----------
    url : str
        Url to be requested.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with the search results.

    Raises
    ------
    AssertionError
        If nothing was found.
    """
    json = get_json(url)
    search_results = json["value"]
    assert search_results, "Nothing was found."
    return DataFrame(search_results)
