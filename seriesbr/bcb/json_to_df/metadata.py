import pandas as pd


def build_df(json):
    """Convert a BCB time series metadata into a DataFrame."""
    metadata = json["result"]["results"][0]
    return pd.DataFrame.from_dict(metadata, orient="index", columns=["values"])
