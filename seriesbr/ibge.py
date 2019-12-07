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
    brazil=None,
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

    microregion : str or int a list of them
        Codes of the microregion to be selected.

    mesoregion : str or int a list of them
        Codes of the mesoregions to be selected.

    classifications : dict
        { classification : [categories], ... }

    Returns
    -------
    A DataFrame with series values and metadata.

    Raises
    ------
    ValueError
        If query produces no values.

    requests.HTTPError
        In case of a bad request.
    """
    baseurl = f"https://servicodados.ibge.gov.br/api/v3/agregados/{code}"
    start, end = parse_dates(start, end, "ibge")
    dates = ibge_build_dates_query(start, end, last_n)
    variables = ibge_build_variables_query(variables)
    locations = ibge_build_location_query(city, state, macroregion, microregion, mesoregion, brazil)
    classifications = ibge_build_classification_query(classifications)
    url = f"{baseurl}{dates}{variables}?{classifications}{locations}&view=flat"
    try:
        return parse_ibge_response(url)
    except requests.exceptions.HTTPError:
        dates = ibge_build_dates_query(start, end, last_n, month=False)
        url = f"{baseurl}{dates}{variables}?{classifications}{locations}&view=flat"
        return parse_ibge_response(get_json(url))


## List Metadata Functions


def list_aggregates(*search, where="nome"):
    """
    Function to list all aggregated variables of IBGE.

    Parameters
    ----------
    search : str
        String to search.

    where : str
        Where to search.

    Returns
    -------
    A DataFrame with metadata about the aggregates.
    """
    json = requests.get("https://servicodados.ibge.gov.br/api/v3/agregados").json()
    df = pd.io.json.json_normalize(json, record_path="agregados")
    if search:
        return do_search(df, search, where)
    return df


def list_variables(aggregate_code):
    """
    Function to list all variables associated with an aggregate of IBGE.

    Parameters
    ----------
    search : str
        String to search.

    where : str
        Where to search.

    Returns
    -------
    A DataFrame with metadata about the variables.
    """
    baseurl = "https://servicodados.ibge.gov.br/api/v3"
    query = f"/agregados/{aggregate_code}/variaveis/all?localidades=BR"
    url = f"{baseurl}{query}"
    json = get_json(url)
    return pd.io.json.json_normalize(json).iloc[:, :3]


def list_periods(aggregate_code):
    """
    Function to list periods of a given aggregate.

    Returns
    -------
    A DataFrame with the frequency, initial and
    final dates.
    """
    baseurl = "https://servicodados.ibge.gov.br/api/v3"
    query = f"/agregados/{aggregate_code}/metadados"
    url = f"{baseurl}{query}"
    json = get_json(url)["periodicidade"]
    df = pd.DataFrame.from_dict(json, orient="index", columns=["value"])
    df.index = ["frequency", "start", "end"]
    return df


def list_classifications(aggregate_code, *search, where="nome"):
    """
    Function to list all classification of a given aggregate.

    Parameters
    ----------
    search : str
        String to search.

    where : str
        Where to search.

    Returns
    -------
    A DataFrame with the classifications and their categories.
    """
    baseurl = "https://servicodados.ibge.gov.br/api/v3/agregados"
    url = f"{baseurl}/{aggregate_code}/metadados"
    json = get_json(url)
    df1 = pd.io.json.json_normalize(json, ['classificacoes', 'categorias'], meta=['classificacoes'])
    df2 = df1.classificacoes.apply(pd.Series).iloc[:, :2]
    df2 = df2.rename(lambda x: "classificacao_" + x, axis='columns')
    df = pd.concat([df1.drop('classificacoes', axis='columns'), df2], axis='columns')
    if search:
        return do_search(df, search, where)
    return df


def list_states(*search, where="nome"):
    """
    Function to list all states and their codes.

    Parameters
    ----------
    search : str
        String to search.

    where : str
        Where to search.

    Returns
    -------
    A DataFrame with metadata about the states.
    """
    url = "https://servicodados.ibge.gov.br/api/v1/localidades/estados/"
    json = get_json(url)
    df = clean_json(json)
    if search:
        return do_search(df, search, where)
    return df


def list_macroregions(*search, where="nome"):
    """
    Function to list all macroregions and their codes.

    Parameters
    ----------
    search : str
        String to search.

    where : str
        Where to search.

    Returns
    -------
    A DataFrame with metadata about the about the states.
    """
    url = "https://servicodados.ibge.gov.br/api/v1/localidades/regioes"
    json = get_json(url)
    df = clean_json(json)
    if search:
        return do_search(df, search, where)
    return df


def list_cities(*search, where="nome"):
    """
    Function to lsit all cities and their codes.

    Parameters
    ----------
    search : str
        String to search.

    where : str
        Where to search.

    Returns
    -------
    A DataFrame with metadata about the cities.
    """
    url = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios"
    json = get_json(url)
    df = clean_json(json)
    if search:
        return do_search(df, search, where)
    return df


def list_microregions(*search, where="nome"):
    """
    Function to lsit all microregions.

    Parameters
    ----------
    search : str
        String to search.

    where : str
        Where to search.

    Returns
    -------
    A DataFrame with metadata about the microregions.
    """
    url = "https://servicodados.ibge.gov.br/api/v1/localidades/microrregioes"
    json = get_json(url)
    df = clean_json(json)
    if search:
        return do_search(df, search, where)
    return df


def list_mesoregions(*search, where="nome"):
    url = "https://servicodados.ibge.gov.br/api/v1/localidades/mesorregioes"
    json = get_json(url)
    df = clean_json(json)
    if search:
        return do_search(df, search, where)
    return df

## Helpers


def clean_json(json):
    """
    Helper function to transform JSON into
    a DataFrame and clean its columns names.
    """
    df = pd.io.json.json_normalize(json, sep='_')
    df = df.rename(lambda x: x.replace('.', '_'), axis='columns')
    df = df.rename(lambda x: '_'.join(re.split(r'_', x)[-2:]), axis='columns')
    return df


def do_search(df, search, where, prefix=""):
    """
    Helper function to search for regex
    in a given column
    """
    # (?iu) sets unicode and ignore case flags
    to_search = r'(?iu)' + '|'.join(search)
    return df.query(f"{where}.str.contains(@to_search)", engine='python')
