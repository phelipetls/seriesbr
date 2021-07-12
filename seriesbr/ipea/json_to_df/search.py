import pandas as pd


def build_df(json):
    """Search IPEA database."""
    search_results = json["value"]
    assert search_results, "Nothing was found."
    return pd.DataFrame(search_results)
