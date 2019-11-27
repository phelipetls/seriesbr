import pandas as pd
from datetime import datetime


def parse_response(response, code, nome, source):
    if source == "bcb":
        return parse_bcb_json(response, code, nome)
    elif source == "ipea":
        return parse_ipea_json(response, code, nome)
    else:
        print("Invalid source.")
        return


def parse_bcb_json(response, code, nome):
    json = response.json()
    assert json, print(f"Request for {code} returned nothing.")
    return json_to_dataframe(json, code, nome, "data", "valor", "%d/%m/%Y")


def parse_ipea_json(response, code, nome):
    json = response.json()["value"]
    assert json, print(f"Request for {code} returned nothing.")
    return json_to_dataframe(json, code, nome, "VALDATA", "VALVALOR", "%Y-%m-%dT%H:%M:%S%z")


def json_to_dataframe(json, code, nome, date_key, value_key, date_fmt):
    D = {"date": [], "value": []}
    date_value_generator = ((item[date_key], item[value_key]) for item in json)
    for date, value in date_value_generator:
        D["date"].append(datetime.strptime(date, date_fmt).strftime("%d/%m/%Y"))
        D["value"].append(value)
    dataframe = pd.DataFrame(D)
    dataframe["date"] = pd.to_datetime(dataframe["date"], format="%d/%m/%Y")
    dataframe["value"] = dataframe["value"].astype("float64")
    dataframe = dataframe.set_index("date").rename(columns={"value": nome if nome else code})
    return dataframe
