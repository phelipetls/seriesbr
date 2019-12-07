from pandas import DataFrame
from .request import get_json

metadata_list = ["codigo_sgs", "title", "periodicidade", "unidade_medida"]


def return_search_results_bcb(url):
    json = get_json(url)
    search_results = json["result"]["results"]
    assert search_results, "Nothing was found."
    return DataFrame(search_results).loc[:, metadata_list]


def return_search_results_ipea(url):
    json = get_json(url)
    search_results = json["value"]
    assert search_results, "Nothing was found."
    return DataFrame(search_results)
