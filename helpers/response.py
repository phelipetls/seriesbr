from pandas import read_json
from pandas import DataFrame, Timestamp
from datetime import date


def parse_response(response, cod, nome, out, source):
    if out == "raw":
        return response.text
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
        print(f"Request for {cod} produces invalid json.")
        raise
    return df.set_index("data").rename(columns={"valor": nome if nome else cod})


def parse_ipea_json(response, cod, nome):
    json = response.json()["value"]
    if json == []:
        raise ValueError(f"Request for {cod} returns no values.")
    return to_dataframe(json).rename(columns={"value": nome if nome else cod})


def to_dataframe(json):
    series_dict = {"date": [], "value": []}
    for item in json:
        obs_date = date(item["ANO"], item["MES"], item["DIA"]).strftime("%d/%m/%Y")
        series_dict["date"].append(Timestamp(obs_date))
        obs_value = item["VALVALOR"]
        series_dict["value"].append(obs_value)
    return DataFrame(series_dict).set_index("date")
