import pandas as pd


def build_df(json):
    metadata = json["value"][0]
    df = pd.DataFrame.from_dict(metadata, orient="index", columns=["values"])
    return df
