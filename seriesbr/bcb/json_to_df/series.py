import pandas as pd


def build_df(json, code, label):
    """Convert a BCB time series in JSON format into a DataFrame."""
    df = pd.DataFrame(json)

    # this columns should be float
    df["valor"] = df["valor"].astype("float64")

    # properly set a datetime index
    df = df.set_index("data")
    df = df.rename_axis("Date")
    df.index = pd.to_datetime(df.index, format="%d/%m/%Y")

    df.columns = [label if label else code]
    return df
