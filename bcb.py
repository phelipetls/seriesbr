import requests
import pandas as pd
from helpers.dates import parse_date


def get(cod, start=None, end=None, last_n=None, convert=True):
    base_url = f"http://api.bcb.gov.br/dados/serie/bcdata.sgs.{cod}/dados"
    formato = "?formato=json"
    if last_n:
        url = base_url + f"/ultimos/{last_n + 1}?formato=json"
    else:
        data = get_dates(start, end)
        url = base_url + formato + data
    return pd.read_json(requests.get(url).text)


def get_dates(start, end):
    start = parse_date(start, start=True) if start else start
    end = parse_date(end, start=False) if end else end
    if start and end:
        data = f"&dataInicial={start}&dataFinal={end}"
    elif start:
        data = f"&dataInicial={start}"
    elif end:
        data = f"&dataFinal={end}"
    else:
        data = ""
    return data
