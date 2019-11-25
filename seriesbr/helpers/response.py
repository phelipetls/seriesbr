from pandas import read_json
from pandas import DataFrame, Timestamp
from datetime import datetime as dt


def parse_response(response, cod, nome, out, source):
    if out == "json":
        return response.json()
    elif out == "pd":
        if source == "bcb":
            return parse_bcb_json(response, cod, nome)
        elif source == "ipea":
            return parse_ipea_json(response, cod, nome)
        else:
            raise ValueError("Invalid source.")
    else:
        return "{out.capitalize()} is not a valid output format."


def parse_bcb_json(response, cod, nome):
    try:
        df = read_json(response.text, dtype={"data": "datetime64", "valor": "float"})
    except ValueError:
        print(f"Request for {cod} produced invalid json.")
        raise
    return df.set_index("data").rename(columns={"valor": nome if nome else cod})


def parse_ipea_json(response, cod, nome):
    json = response.json()["value"]
    if json == []:
        raise ValueError(f"Request for {cod} returned nothing.")
    return to_dataframe(json).rename(columns={"value": nome if nome else cod})


def to_dataframe(json):
    series_dict = {"date": [], "value": []}
    for item in json:
        obs_date = dt.strptime(item["VALDATA"], "%Y-%m-%dT%H:%M:%S%z").strftime("%d/%m/%Y")
        series_dict["date"].append(Timestamp(obs_date))
        obs_value = item["VALVALOR"]
        series_dict["value"].append(obs_value)
    return DataFrame(series_dict).set_index("date")
