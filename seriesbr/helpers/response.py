import pandas as pd
from datetime import datetime


def parse_response(response, code, name, source):
    if source == "bcb":
        return parse_bcb_json(response, code, name)
    elif source == "ipea":
        return parse_ipea_json(response, code, name)


def parse_bcb_json(response, code, name):
    json = response.json()
    assert json, print(f"Request for {code} returned nothing.")
    return json_to_dataframe(json, code, name, "data", "valor", "%d/%m/%Y")


def parse_ipea_json(response, code, name):
    json = response.json()["value"]
    assert json, print(f"Request for {code} returned nothing.")
    return json_to_dataframe(json, code, name, "VALDATA", "VALVALOR", "%Y-%m-%dT%H:%M:%S%z")


def json_to_dataframe(json, code, name, date_key, value_key, date_fmt):
    df = pd.DataFrame(json)
    df[date_key] = convert_to_datetime(df[date_key].values, date_fmt=date_fmt)
    df[date_key] = pd.to_datetime(df[date_key], format="%d/%m/%Y")
    df[value_key] = df[value_key].astype('float64')
    df = df.set_index(date_key)
    df.columns = [name if name else code]
    df = df.rename_axis("date")
    return df


@pd.np.vectorize
def convert_to_datetime(date_string, date_fmt):
    return datetime.strptime(date_string, date_fmt).strftime("%d/%m/%Y")
