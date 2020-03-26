import pandas as pd
from .request import get_json


def bcb_json_to_df(url, code, name):
    """
    Parse a timeseries returned by BCB API
    into a DataFrame.
    """
    json = get_json(url)
    df = pd.DataFrame(json)
    df["valor"] = df["valor"].astype("float64")
    df = df.set_index("data")
    df = df.rename_axis("Date")
    df.index = pd.to_datetime(df.index, format="%d/%m/%Y")
    df.columns = [name if name else code]
    return df


def ipea_json_to_df(url, code, name):
    """
    Parse a timeseries returned by IPEA API
    into a DataFrame.
    """
    json = get_json(url)["value"]
    df = pd.DataFrame(json)

    # removing utc component from date string
    try:
        df["VALDATA"] = df["VALDATA"].str[:-6]
        df = df.set_index("VALDATA")
        df = df.rename_axis("Date")
        df.index = pd.to_datetime(df.index, format="%Y-%m-%dT%H:%M:%S")
        # casting numerical values
        df["VALVALOR"] = pd.to_numeric(df["VALVALOR"], errors="coerce")
        df.columns = [name if name else code]
    except KeyError:
        return

    return df


def ibge_json_to_df(url, freq="mensal"):
    """
    Parse a IBGE table/aggregate in JSON format
    into a DataFrame.
    """
    json = get_json(url)
    # ignore first element as it as no real data
    df = pd.DataFrame(json[1:])
    # getting columns names
    df.columns = json[0].values()

    # handling dates
    date_fmt = "%Y" if freq == "anual" else "%Y%m"
    date_key = json[0]["D2C"]
    df[date_key] = pd.to_datetime(df[date_key], format=date_fmt)
    df = df.set_index(date_key)
    df = df.rename_axis("Date")

    # handling numerical values
    df["Valor"] = pd.to_numeric(df["Valor"], errors="coerce")

    # getting location code name column
    location_key = json[0]["D1C"]

    # dropping less useful columns
    # i.e., any columns which represents code,
    # except for the location and variable code,
    # and a bunch of other columns
    df = df.drop(
        [
            c
            for c in df.columns
            if c.endswith("(Código)") and c not in [location_key, "Variável (Código)"]
        ]
        + ["Mês", "Unidade de Medida", "Brasil", "Nível Territorial"],
        axis="columns",
        errors="ignore",
    )
    return df
