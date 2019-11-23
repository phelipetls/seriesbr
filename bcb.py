import pandas as pd
from helpers.dates import parse_date
from helpers.types import parse_args
from helpers.response import parse_response
from helpers.request import get_serie


def get(cod, nome=None, start=None, end=None, last_n=None, out="pd"):
    base_url = f"http://api.bcb.gov.br/dados/serie/bcdata.sgs.{cod}/dados"
    formato = "?formato=json"
    if last_n:
        url = base_url + f"/ultimos/{last_n + 1}?formato=json"
    else:
        data = get_dates(start, end)
        url = base_url + formato + data
    return parse_response(get_serie(url), cod, nome, out, source="bcb")


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


def get_series(*args, start=None, end=None, last_n=None, join="outer", **kwargs):
    codigos, nomes = parse_args(*args)
    return pd.concat(
        [get(cod, start, end, last_n) for cod in codigos],
        axis="columns",
        join=join,
        **kwargs
    ).rename(columns={cod: nome for nome, cod in zip(nomes, codigos)})
