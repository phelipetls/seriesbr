import pandas as pd


def bcb_json_to_df(json, code, name):
    """
    Auxiliary function to convert json produced by
    BCB's and IPEA's API into a DataFrame.
    """
    assert json, print(f"Request for {code} returned nothing.")
    df = pd.DataFrame(json)
    df["data"] = pd.to_datetime(df["data"], format="%d/%m/%Y")
    df["valor"] = df["valor"].astype('float64')
    df = df.set_index("data")
    df = df.rename_axis("Date")
    df.columns = [name if name else code]
    return df


def ipea_json_to_df(json, code, name):
    """
    Auxiliary function to convert json produced by
    BCB's and IPEA's API into a DataFrame.
    """
    json = json["value"]
    assert json, print(f"Request for {code} returned nothing.")
    df = pd.DataFrame(json)
    df["VALDATA"] = df["VALDATA"].str[:-6]
    df["VALDATA"] = pd.to_datetime(df["VALDATA"], format="%Y-%m-%dT%H:%M:%S")
    df["VALVALOR"] = df["VALVALOR"].astype('float64')
    df = df.set_index("VALDATA")
    df = df.rename_axis("Date")
    df.columns = [name if name else code]
    return df


def ibge_json_to_df(json, freq="mensal"):
    """
    Auxiliary function to convert json produced by
    IBGE's API into a DataFrame.
    """
    assert len(json) > 1, "This request produced no value."
    df = pd.DataFrame(json[1:])
    df.columns = json[0].values()
    date_fmt = "%Y%m" if freq == "mensal" else "%Y"
    date_key = json[0]["D2C"]
    df[date_key] = pd.to_datetime(df[date_key], format=date_fmt)
    df["Valor"] = pd.to_numeric(df["Valor"], errors="coerce")
    df = df.set_index(date_key)
    df = df.rename_axis("Date")
    df = df.drop(
        [c for c in df.columns if c.endswith("(Código)")]
        + ["Mês", "Unidade de Medida", "Brasil"],
        axis="columns",
        errors="ignore",
    )
    return df
