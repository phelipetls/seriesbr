from pandas import concat
from helpers.types import parse_cods
from helpers.request import get_serie
from helpers.response import parse_response


def get(cod, nome=None, start=None, end=None, out="pd"):
    base_url = "http://ipeadata2-homologa.ipea.gov.br/api/v1/ValoresSerie(SERCODIGO='"
    url = base_url + cod + "')"
    return parse_response(get_serie(url), cod, nome, out, source="ipea")


def get_series(*codigos, start=None, end=None, last_n=None, join="outer", **kwargs):
    codigos, nomes = parse_cods(*codigos)
    return concat(
        [get(cod, start, end) for cod in codigos],
        axis="columns",
        join=join,
        sort=True,  # done to avoid pandas warning messages
        **kwargs
    ).rename(columns={cod: nome for nome, cod in zip(nomes, codigos)})
