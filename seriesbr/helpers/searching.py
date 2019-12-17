from pandas import DataFrame
from .request import get_json

metadata_list = ["codigo_sgs", "title", "periodicidade", "unidade_medida"]


def get_search_results_bcb(url):
    """
    Auxiliary function to request BCB's search
    results and turn json into a DataFrame.
    """
    json = get_json(url)
    search_results = json["result"]["results"]
    assert search_results, "Nothing was found."
    return DataFrame(search_results).loc[:, metadata_list]


def get_search_results_ipea(url):
    """
    Auxiliary function to request IPEA's search
    results and turn json into a DataFrame.
    """
    json = get_json(url)
    search_results = json["value"]
    assert search_results, "Nothing was found."
    return DataFrame(search_results)
