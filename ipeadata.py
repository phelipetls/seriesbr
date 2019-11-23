import requests
from pandas import concat
from helpers.types import parse_cods
from helpers.request import custom_get
from helpers.response import parse_response
from helpers.formatter import format_results_ipea


def get(cod, nome=None, start=None, end=None, out="pd"):
    base_url = "http://ipeadata2-homologa.ipea.gov.br/api/v1/ValoresSerie(SERCODIGO='"
    url = base_url + cod + "')"
    return parse_response(custom_get(url).text, cod, nome, out, source="ipea")


def get_series(*codigos, start=None, end=None, last_n=None, join="outer", **kwargs):
    codigos, nomes = parse_cods(*codigos)
    return concat(
        [get(cod, start, end) for cod in codigos],
        axis="columns",
        join=join,
        sort=True,  # done to avoid pandas warning messages
        **kwargs
    ).rename(columns={cod: nome for nome, cod in zip(nomes, codigos)})


def search(name):
    baseurl = "http://ipeadata2-homologa.ipea.gov.br/api/v1/Metadados?$select=SERCODIGO,SERNOME"
    url = baseurl + f"&$filter=contains(SERNOME,'{name}')"
    results = custom_get(url).json()["value"]
    format_results_ipea(results)
