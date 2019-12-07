import re
import requests
import pandas as pd
from .helpers.request import get_json
from .helpers.response import parse_ibge_response
from .helpers.dates import parse_dates
from .helpers.url import (
    ibge_build_dates_query,
    ibge_build_variables_query,
    ibge_build_location_query,
    ibge_build_classification_query,
)


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
    classifications=None,
):
    """
    Function to get variables associated with a aggregated variable of IBGE's
    SIDRA database.

    Parameters
    ----------
    code : int
    The code of the aggregated variable.

    variables : int or list of ints
    Which variables to select (if None, return all of them).

    start : int or str
    Initial date in the format %Y or %Y%m.

    end : int or str
    Final date in the format %Y or %Y%m.

    last_n : int or str
    Return only last n observations.

    city : str or int a list of them
    Codes of the cities to be selected.

    state : str or int a list of them
    Codes of the states to be selected.

    macroregion : str or int a list of them
    Codes of the macroregions to be selected.

    For example, Sudeste, Sul, etc.

    microregion : str or int a list of them
    Codes of the microregion to be selected.

    For example, Lagos, Rio de Janeiro, Itaguaí are
    microregions of the state of Rio de Janeiro.

    mesoregion : str or int a list of them
    Codes of the mesoregions to be selected.

    For example, Baixadas, Região Metropolitana,
    Norte Fluminense etc. are mesoregions of the
    state of Rio de Janeiro.

    Returns
    -------
    A DataFrame with series values and metadata.
    """
    baseurl = f"https://servicodados.ibge.gov.br/api/v3/agregados/{code}"
    dates = build_dates_query(start, end, last_n)
    variables = build_variables_query(variables)
    locality = build_locality_query(city, state, macroregion, microregion, mesoregion)
    classifications = build_classification_query(classifications)
    url = f"{baseurl}{dates}{variables}?{classifications}{locality}&view=flat"
    try:
        return parse_ibge_response(custom_get(url).json())
    except requests.exceptions.HTTPError:
        dates = build_dates_query(start, end, last_n, monthly=False)
        url = f"{baseurl}{dates}{variables}?{classifications}{locality}&view=flat"
        return parse_ibge_response(custom_get(url).json())


# Functions to help build url

def build_classification_query(classifications=None):
    if isinstance(classifications, dict):
        s = []
        for classification, category in classifications.items():
            if not category or category == "all":
                s.append(f"{classification}[all]")
            else:
                s.append(f"{classification}[{cat(category, ',')}]")
        return "classificacao=" + "|".join(s)
    else:
        return ""


def build_dates_query(start=None, end=None, last_n=None, monthly=True):
    """
    Auxiliary function to build the date part
    of the url.

    It depends if date
    """
    if monthly:
        today = datetime.today().strftime('%Y%m')
    else:
        today = datetime.today().strftime('%Y')
        start = start[:-2] if start else start
        end = end[:-2] if end else end
    if last_n:
        return f"/periodos/-{last_n}"
    elif start and end:
        dates = f"/periodos/{start}-{end}"
    elif start:
        dates = f"/periodos/{start}-{today}"
    elif end:
        dates = f"/periodos/190001-{end}"
    else:
        dates = f"/periodos/-10000000"
    return dates


def build_variables_query(variables):
    if isiterable(variables):
        return f"/variaveis/{cat(variables, '|')}"
    elif variables:
        return f"/variaveis/{variables}"
    else:
        return f"/variaveis"


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
        return parse_ibge_response(get_json(url))


## List Metadata Functions

def list_aggregates(search=None, where="nome"):
    """
    Function to list all aggregated variables of IBGE.

    Parameters
    ----------
    search : str
    String to search.

    search_in : str
    Where to search.

    Returns
    -------
    A DataFrame with information regarding the aggregates.
    """
    json = requests.get("https://servicodados.ibge.gov.br/api/v3/agregados").json()
    df = pd.io.json.json_normalize(json, record_path="agregados")
    if search:
        return df.query(f'{where}.str.contains(@search)', engine='python')
    return df


def list_variables(aggregate_code):
    """
    Function to list all variables associated with an aggregate of IBGE.

    Parameters
    ----------
    search : str
    String to search.

    search_in : str
    Where to search.

    Returns
    -------
    A DataFrame with information regarding the variables.
    """
    baseurl = "https://servicodados.ibge.gov.br/api/v3"
    query = f"/agregados/{aggregate_code}/variaveis/all?localidades=BR"
    url = f"{baseurl}{query}"
    json = get_json(url)
    return pd.io.json.json_normalize(json).iloc[:, :3]


def list_classifications(aggregate_code, search=None, where="nome"):
    baseurl = "https://servicodados.ibge.gov.br/api/v3/agregados"
    url = f"{baseurl}/{aggregate_code}/metadados"
    json = custom_get(url).json()
    df1 = pd.io.json.json_normalize(json, ['classificacoes', 'categorias'], meta=['classificacoes'])
    df2 = df1.classificacoes.apply(pd.Series).iloc[:, :2]
    df2 = df2.rename(lambda x: "classificacao_" + x, axis='columns')
    df = pd.concat([df1.drop('classificacoes', axis='columns'), df2], axis='columns')
    if search:
        return df.query(f'{where}.str.contains(@search)', engine='python')
    return df


def list_states(search=None, where="nome"):
    """
    Function to list all states and their codes.

    Returns
    -------
    A DataFrame with information about the states.
    """
    url = "https://servicodados.ibge.gov.br/api/v1/localidades/estados/"
    json = get_json(url)
    df = clean_json(json)
    if search:
        return df.query(f'{where}.str.contains(@search)', engine='python')
    return df


def list_macroregions(search=None, where="nome"):
    """
    Function to list all macroregions and their codes.

    Returns
    -------
    A DataFrame with information about the states.
    """
    url = "https://servicodados.ibge.gov.br/api/v1/localidades/regioes"
    json = get_json(url)
    df = clean_json(json)
    if search:
        return df.query(f'{where}.str.contains(@search)', engine='python')
    return df


def list_cities(search=None, where="nome"):
    url = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios"
    json = get_json(url)
    df = clean_json(json)
    if search:
        return df.query(f'{where}.str.contains(@search)', engine='python')
    return df


def list_microregions(search=None, where="nome"):
    url = "https://servicodados.ibge.gov.br/api/v1/localidades/microrregioes"
    json = get_json(url)
    df = clean_json(json)
    if search:
        return df.query(f'{where}.str.contains(@search)', engine='python')
    return df


def list_mesoregions(search=None, where="nome"):
    url = "https://servicodados.ibge.gov.br/api/v1/localidades/mesorregioes"
    json = get_json(url)
    df = clean_json(json)
    if search:
        return df.query(f'{where}.str.contains(@search)', engine='python')
    return df


def clean_json(json):
    df = pd.io.json.json_normalize(json, sep='_')
    df = df.rename(lambda x: x.replace('.', '_'), axis='columns')
    df = df.rename(lambda x: '_'.join(re.split(r'_', x)[-2:]), axis='columns')
    return df
