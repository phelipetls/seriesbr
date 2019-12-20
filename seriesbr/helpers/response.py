import pandas as pd
from .request import get_json


def bcb_json_to_df(url, code, name):
    """
    Auxiliary function to convert json produced by
    BCB's and IPEA's API into a DataFrame.

    Parameters
    ----------
    url : str
        Url to be requested.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with time series' values and a DateTimeIndex.
    """
    json = get_json(url)
    df = pd.DataFrame(json)
    df["data"] = pd.to_datetime(df["data"], format="%d/%m/%Y")
    df["valor"] = df["valor"].astype('float64')
    df = df.set_index("data")
    df = df.rename_axis("Date")
    df.columns = [name if name else code]
    return df


def ipea_json_to_df(url, code, name):
    """
    Auxiliary function to convert json produced by
    BCB's and IPEA's API into a DataFrame.

    Parameters
    ----------
    url : str
        Url to be requested.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with time series' values and a DateTimeIndex.
    """
    json = get_json(url)["value"]
    df = pd.DataFrame(json)
    df["VALDATA"] = df["VALDATA"].str[:-6]
    df["VALDATA"] = pd.to_datetime(df["VALDATA"], format="%Y-%m-%dT%H:%M:%S")
    df["VALVALOR"] = df["VALVALOR"].astype('float64')
    df = df.set_index("VALDATA")
    df = df.rename_axis("Date")
    df.columns = [name if name else code]
    return df


def ibge_json_to_df(url, freq="mensal"):
    """
    Auxiliary function to convert json produced by
    IBGE's API into a DataFrame.

    Parameters
    ----------
    url : str
        Url to be requested.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with time series' values, metadatas
        and a DateTimeIndex.
    """
    json = get_json(url)
    df = pd.DataFrame(json[1:])
    df.columns = json[0].values()
    date_fmt = "%Y" if freq == "anual" else "%Y%m"
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
