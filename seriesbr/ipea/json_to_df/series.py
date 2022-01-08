import pandas as pd


def build_df(json, code, label):
    json = json["value"]
    df = pd.DataFrame(json)

    # removing utc component from date string
    try:
        df["VALDATA"] = df["VALDATA"].str[:-6]
        df = df.set_index("VALDATA")
        df = df.rename_axis("Date")
        df.index = pd.to_datetime(df.index, format="%Y-%m-%dT%H:%M:%S")
        # casting numerical values
        df["VALVALOR"] = pd.to_numeric(df["VALVALOR"], errors="coerce")
        df.columns = [label if label else code]
    except KeyError:
        return

    return df
