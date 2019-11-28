from pandas import DataFrame


def return_search_results_bcb(response):
    json = response.json()
    search_results = json["result"]["results"]
    assert search_results, "Nothing was found."
    metadata_list = ["codigo_sgs", "title", "periodicidade", "unidade_medida"]
    D = {metadata: [] for metadata in metadata_list}
    for result in search_results:
        for metadata in metadata_list:
            D[metadata].append(result[metadata])
    df = DataFrame(D)
    return df


def return_search_results_ipea(response):
    search_results = response.json()["value"]
    assert search_results, "Nothing was found."
    D = {metadata: [] for metadata in search_results[0].keys()}
    for result in search_results:
        for metadata in result.keys():
            D[metadata].append(result[metadata])
    df = DataFrame(D)
    return df
