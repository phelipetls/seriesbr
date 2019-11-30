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
# Functions to help build url

def build_classification_query(classifications=None):
    if isinstance(classifications, dict):
        s = []
        for classification, category in classifications.items():
            if not category or category == "all":
                s.append(f"{classification}[all]")
            else:
                s.append(f"{classification}[{cat(category, ',') if isiterable(category) else category}]")
        return "classificacao=" + "|".join(s)
    else:
        return ""


def build_variables_query(variables):
    if isiterable(variables):
        return f"variaveis/{pipe(variables)}"
    elif variables:
        return f"variaveis/{variables}"
    else:
        return f"variaveis"


    else:
        return date_filter(start, end)


def build_locality_query(city, state, macroregion, microregion, mesoregion):
    # note-to-self: http://api.sidra.ibge.gov.br/desctabapi.aspx?c=136
    base = "&localidades="
    query = []
    if city:
        query.append(f"N6[{cat(city, '|') if city != 'all' else city}]")
    if state:
        query.append(f"N3[{cat(state, ',') if state != 'all' else state}]")
    if macroregion:
        query.append(f"N2[{cat(macroregion, ',') if macroregion != 'all' else macroregion}]")
    if mesoregion:
        query.append(f"N7[{cat(mesoregion, ',') if mesoregion != 'all' else mesoregion}]")
    if microregion:
        query.append(f"N9[{cat(microregion, ',') if microregion != 'all' else microregion}]")
    if all([local is None for local in [city, state, macroregion, microregion, mesoregion]]):
        return f"{base}BR"
    return base + "|".join(query)


def get_metadata(code):
    """
    This function prints metadata information
    about a given aggregated variable.

    Parameters
    ----------
    code (str or int): variable's code.

    Returns
    -------
    None.
    """
    baseurl = "https://servicodados.ibge.gov.br/api/v3/agregados"
    url = f"{baseurl}/{code}/metadados"
    json = custom_get(url).json()
    newline = "\n"
    double_newline = "\n\n"
    spaces = "\t"
    description = f"""
    Id:   {json['id']}
    Nome: {json['nome']}
    Url:  {json['URL']}

    Níveis Territoriais: {', '.join(json['nivelTerritorial']['Administrativo'])}

    {', '.join(['{}: {}'.format(metadata.capitalize(), value) for metadata, value in json['periodicidade'].items()])}

    Variáveis:

    {
    newline.join(
            [
                "{} {} {}".format(spaces, variavel["id"], variavel["nome"])
                for variavel in json["variaveis"]
            ]
        )
    }

    Classificações e categorias:

{double_newline.join(
    [
        "{} {} ({}): ".format(" " * 3, classificacao["nome"], classificacao["id"])
        + f"{newline}{spaces}"
        + f", {newline}{spaces}".join(
            [
                "{} - {}".format(categoria["id"], categoria["nome"])
                for categoria in classificacao["categorias"]
            ]
        )
        for classificacao in json["classificacoes"]
    ]
)}
    """
    print(description)


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


## List Metadata Functions

def list_aggregates(search=None):
    json = requests.get("https://servicodados.ibge.gov.br/api/v3/agregados").json()
    df = pd.io.json.json_normalize(json, record_path="agregados")
    if search:
        return df.query('nome.str.contains(@search)', engine='python')
    return df


def list_variables(aggregate_code):
    baseurl = "https://servicodados.ibge.gov.br/api/v3"
    query = f"/agregados/{aggregate_code}/variaveis/all?localidades=BR"
    url = f"{baseurl}{query}"
    json = custom_get(url).json()
    return pd.io.json.json_normalize(json).iloc[:, :3]


def list_states(*codes):
    url = "https://servicodados.ibge.gov.br/api/v1/localidades/estados/"
    json = custom_get(url).json()
    df = pd.io.json.json_normalize(json)
    df = df.rename(lambda x: x.replace('.', '_'), axis='columns')
    return clean_json(json)


def list_macroregions(*codes):
    url = "https://servicodados.ibge.gov.br/api/v1/localidades/regioes"
    json = custom_get(url).json()
    return clean_json(json)


def list_cities(*codes, state=None, macroregion=None, microregion=None, mesoregion=None):
    url = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios"
    json = custom_get(url).json()
    return clean_json(json)


def list_microregions(*codes, state=None, macroregion=None, mesoregion=None):
    url = "https://servicodados.ibge.gov.br/api/v1/localidades/microrregioes"
    json = custom_get(url).json()
    return clean_json(json)


def list_mesoregions(*codes, macroregion=None):
    url = "https://servicodados.ibge.gov.br/api/v1/localidades/mesorregioes"
    json = custom_get(url).json()
    return clean_json(json)


def clean_json(json):
    df = json_normalize(json, sep='_')
    df = df.rename(lambda x: x.replace('.', '_'), axis='columns')
    df = df.rename(lambda x: '_'.join(re.split(r'_', x)[-2:]), axis='columns')
    return df
