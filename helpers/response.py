from pandas import read_json
from json import loads
from pandas import DataFrame
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


def parse_bcb_json(raw_json, cod, nome):
    try:
        json_df = read_json(raw_json, dtype={"data": "datetime64", "valor": "float"})
    except ValueError:
        print(f"Request for {cod} produces invalid json.")
        raise
    return json_df.set_index("data").rename(columns={"valor": nome if nome else cod})


def parse_ipea_json(raw_json, cod, nome):
    json_values = loads(raw_json)["value"]
    if json_values == []:
        raise ValueError(f"Request for {cod} returns no values.")
    return DataFrame([
        {
            "date": date(item["ANO"], item["MES"], item["DIA"]).strftime("%d/%m/%Y"),
            "value": item["VALVALOR"],
        }
        for item in json_values
    ]).set_index("date").rename(columns={"value": nome if nome else cod})
