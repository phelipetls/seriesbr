import pandas as pd


def build_df(json):
    """Convert a IBGE time series metadata into a DataFrame."""
    return pd.DataFrame.from_dict(json, orient="index", columns=["values"])
