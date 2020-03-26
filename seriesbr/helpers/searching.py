from pandas import DataFrame
from .request import get_json

metadata_list = ["codigo_sgs", "title", "periodicidade", "unidade_medida"]


def bcb_get_search_results(url):
    """
    Request a BCB search result (CKAN API) and parse it into
    a DataFrame. Get only the columns in `metadata_list`.
    """
    json = get_json(url)
    search_results = json["result"]["results"]
    assert search_results, "Nothing was found."
    return DataFrame(search_results).loc[:, metadata_list]


def ipea_get_search_results(url):
    """
    Request a IPEA search result and parse it into a
    DataFrame.
    """
    json = get_json(url)
    search_results = json["value"]
    assert search_results, "Nothing was found."
    return DataFrame(search_results)
