import requests
from helpers.json import clean_json


def get(cod, start=None, end=None):
    base_url = "http://ipeadata2-homologa.ipea.gov.br/api/v1/ValoresSerie(SERCODIGO='"
    url = base_url + cod + "')"
    return clean_json(requests.get(url).text)
