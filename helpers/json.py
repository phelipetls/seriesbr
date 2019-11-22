import json
import pandas as pd
import datetime as dt


def clean_json(raw_json):
    json_values = json.loads(raw_json)["value"]
    return pd.DataFrame([
        {
            "date": dt.date(item["ANO"], item["MES"], item["DIA"]).strftime("%d/%m/%Y"),
            "value": item["VALVALOR"],
        }
        for item in json_values
    ])
