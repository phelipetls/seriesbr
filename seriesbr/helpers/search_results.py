from pandas import DataFrame
from .request import get_json

metadata_list = ["codigo_sgs", "title", "periodicidade", "unidade_medida"]


def bcb_get_search_results(url):
    """Search BCB database through CKAN API."""
    json = get_json(url)
    search_results = json["result"]["results"]
    assert search_results, "Nothing was found."
    return DataFrame(search_results).loc[:, metadata_list]


def ipea_get_search_results(url):
    """Search IPEA database."""
    json = get_json(url)
    search_results = json["value"]
    assert search_results, "Nothing was found."
    return DataFrame(search_results)
