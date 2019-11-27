from pandas import DataFrame


def return_search_results_bcb(response):
    json = response.json()
    count = json["result"]["count"]
    search_results = json["result"]["results"]
    assert search_results, "Nothing was found."
    metadata_list = ["codigo_sgs", "periodicidade", "unidade_medida", "title"]
    D = {metadata: [] for metadata in metadata_list}
    for result in search_results:
        for metadata in metadata_list:
            D[metadata].append(result[metadata])
    df = DataFrame(D)
    return count, df


def return_search_results_ipea(response):
    search_results = response.json()["value"]
    assert search_results, "Nothing was found."
    D = {metadata: [] for metadata in search_results[0].keys()}
    for result in search_results:
        for metadata in result.keys():
            D[metadata].append(result[metadata])
    df = DataFrame(D)
    return df
