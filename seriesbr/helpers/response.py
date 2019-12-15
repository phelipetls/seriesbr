import pandas as pd
from .request import get_json


def parse_bcb_response(url, code, name):
    json = get_json(url)
    assert json, print(f"Request for {code} returned nothing.")
    return json_to_dataframe(json, code, name, "data", "valor", "%d/%m/%Y")


def parse_ipea_response(url, code, name):
    json = get_json(url)["value"]
    assert json, print(f"Request for {code} returned nothing.")
    return json_to_dataframe(json, code, name, "VALDATA", "VALVALOR", "%Y-%m-%dT%H:%M:%S")


def json_to_dataframe(json, code, name, date_key, value_key, date_fmt):
    df = pd.DataFrame(json)
    if date_fmt == "%Y-%m-%dT%H:%M:%S":
        df[date_key] = df[date_key].str[:-6]
    df[date_key] = pd.to_datetime(df[date_key], format=date_fmt)
    df[value_key] = df[value_key].astype('float64')
    df = df.set_index(date_key)
    df.columns = [name if name else code]
    df = df.rename_axis("Date")
    return df


def parse_ibge_response(url):
    json = get_json(url)
    assert len(json) > 1, "This request produced no value."
    return ibge_json_to_dataframe(json)


def ibge_json_to_dataframe(json):
    df = pd.DataFrame(json[1:])
    date_key = json[0]["D2C"]
    df.columns = json[0].values()
    try:
        df[date_key] = pd.to_datetime(df[date_key], format="%Y%m")
    except ValueError:
        df[date_key] = pd.to_datetime(df[date_key], format="%Y")
    df["Valor"] = pd.to_numeric(df["Valor"], errors="coerce")
    df = df.rename(columns={date_key: "Date"})
    df = df.set_index("Date")
    df = df.drop(
        [c for c in df.columns if c.endswith("(Código)")] + ["Mês", "Unidade de Medida", "Brasil"],
        axis="columns",
        errors="ignore"
    )
    return df
