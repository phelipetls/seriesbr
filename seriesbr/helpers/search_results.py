from pandas import DataFrame


def return_search_results_bcb(json):
    search_results = json["result"]["results"]
    assert search_results, "Nothing was found."
    metadata_list = ["codigo_sgs", "title", "periodicidade", "unidade_medida"]
    return DataFrame(search_results).loc[:, metadata_list]


def return_search_results_ipea(json):
    search_results = json["value"]
    assert search_results, "Nothing was found."
    return DataFrame(search_results)
