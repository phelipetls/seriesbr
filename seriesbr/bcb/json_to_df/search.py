import pandas as pd


def build_df(json):
    """Search BCB database through CKAN API."""
    search_results = json["result"]["results"]
    assert search_results, "Nothing was found."
    return pd.DataFrame(search_results).loc[
        :, ["codigo_sgs", "title", "periodicidade", "unidade_medida"]
    ]
