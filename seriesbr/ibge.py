import re
import requests
from datetime import datetime
from pandas.io.json import json_normalize
from .helpers.request import custom_get
from .helpers.utils import pipe, isiterable


def get_series(
    code,
    variables=None,
    start=None,
    end=None,
    last_n=None,
    city=None,
    state=None,
    macroregion=None,
    microregion=None,
    mesoregion=None,
):
    baseurl = "https://servicodados.ibge.gov.br/api/v3/"
    aggregate = f"agregados/{code}/"
    dates = build_dates_query(start, end, last_n)
    variables = build_variables_query(variables)
    locality = build_locality_query(city, state, macroregion, microregion, mesoregion)
    url = f"{baseurl}{aggregate}{dates}{variables}{locality}"
    print(url)
    return custom_get(url).json()


def build_variables_query(variables):
    if isiterable(variables):
        return f"variaveis/{pipe(variables)}"
    elif variables:
        return f"variaveis/{variables}"
    else:
        return f"variaveis"


def build_dates_query(start, end, last_n):
    if last_n:
        return f"periodos/-{last_n}/"
    else:
        return date_filter(start, end)


def build_locality_query(city, state, macroregion, microregion, mesoregion):
    base = "?localidades"
    if city:
        return f"{base}/N6/{pipe(city)}"
    elif state:
        return f"{base}/N3/{pipe(state)}"
    elif macroregion:
        return f"{base}/N2/{pipe(macroregion)}"
    elif microregion:
        return f"{base}/N3/{pipe(microregion)}"
    elif mesoregion:
        return f"{base}/N7/{pipe(microregion)}"
    else:
        return f"{base}=BR"


def get_metadata(code):
    baseurl = "https://servicodados.ibge.gov.br/api/v3/agregados"
    url = f"{baseurl}/{code}/metadados"
    print(url)
    json = custom_get(url).json()
    return json_normalize(json, record_path=['variaveis'], meta=['id', 'nome'], meta_prefix='agregado_')


def date_filter(start, end):
    """
    Auxiliary function to return the right query
    to filter dates.
    """
    if start and end:
        dates = f"periodos/{start}-{end}/"
    elif start:
        dates = f"periodos/{start}01-{datetime.today().strftime('%Y%m')}/"
    elif end:
        dates = f"periodos/190001-{end}/"
    else:
        dates = ""
    return dates


def list_aggregates():
    json = requests.get("https://servicodados.ibge.gov.br/api/v3/agregados").json()
    return json_normalize(
        json, record_path="agregados", meta=["id", "nome"], meta_prefix="pesquisa_"
    )


def list_variables(aggregate_code):
    baseurl = "https://servicodados.ibge.gov.br/api/v3"
    query = f"/agregados/{aggregate_code}/variaveis/all?localidades=BR"
    url = f"{baseurl}{query}"
    json = custom_get(url).json()
    return json_normalize(json).iloc[:, :3]


def list_states(*codes):
    baseurl = "https://servicodados.ibge.gov.br/api/v1/localidades/estados/"
    url = f"{baseurl}{pipe(codes)}"
    print(url)
    json = custom_get(url).json()
    df = json_normalize(json)
    df = df.rename(lambda x: x.replace('.', '_'), axis='columns')
    return clean_json(json)


def list_macroregions(*codes):
    baseurl = "https://servicodados.ibge.gov.br/api/v1/localidades/regioes/"
    url = f"{baseurl}{pipe(codes)}"
    print(url)
    json = custom_get(url).json()
    return clean_json(json)


def list_cities(*codes, state=None, macroregion=None, microregion=None, mesoregion=None):
    baseurl = "https://servicodados.ibge.gov.br/api/v1/localidades/"
    if state:
        url = f"{baseurl}estados/{pipe(state)}/municipios"
    elif macroregion:
        url = f"{baseurl}regioes/{pipe(macroregion)}/municipios"
    elif microregion:
        url = f"{baseurl}microrregioes/{pipe(microregion)}/municipios"
    elif mesoregion:
        url = f"{baseurl}mesorregioes/{pipe(mesoregion)}/municipios/"
    else:
        url = f"{baseurl}municipios/{pipe(codes)}"
    print(url)
    json = custom_get(url).json()
    return clean_json(json)


def list_microregions(*codes, state=None, macroregion=None, mesoregion=None):
    baseurl = "https://servicodados.ibge.gov.br/api/v1/localidades/"
    if state:
        url = f"{baseurl}estados/{pipe(state)}/microrregioes"
    elif macroregion:
        url = f"{baseurl}regioes/{pipe(macroregion)}/microrregioes"
    elif mesoregion:
        url = f"{baseurl}mesorregioes/{pipe(mesoregion)}/microrregioes"
    elif codes:
        url = f"{baseurl}microrregioes/{pipe(codes)}"
    else:
        url = f"{baseurl}microrregioes"
    print(url)
    json = custom_get(url).json()
    return clean_json(json)


def list_mesoregions(*codes, macroregion=None):
    baseurl = "https://servicodados.ibge.gov.br/api/v1/localidades/"
    if macroregion:
        url = f"{baseurl}regioes/{pipe(macroregion)}/mesorregioes"
    elif codes:
        url = f"{baseurl}mesorregioes/{pipe(codes)}"
    else:
        url = f"{baseurl}mesorregioes"
    print(url)
    json = custom_get(url).json()
    return clean_json(json)


def clean_json(json):
    df = json_normalize(json, sep='_')
    df = df.rename(lambda x: x.replace('.', '_'), axis='columns')
    df = df.rename(lambda x: '_'.join(re.split(r'_', x)[-2:]), axis='columns')
    return df
