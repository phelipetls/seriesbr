import pandas as pd
from .helpers.request import get_json
from .helpers.response import parse_ibge_response
from .helpers.utils import do_search
from .helpers.lists import list_regions
from .helpers.url import (
    ibge_build_dates_query,
    ibge_build_variables_query,
    ibge_build_location_query,
    ibge_build_classification_query,
    locations_dict
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

    variables : int or list of ints, default None
        Which variables to select (if None, return all of them).

    start : int or str, default None
        Initial date, year last.

    end : int or str, default None
        Final date, year last.

    last_n : int or str, default None
        Return only last n observations.

    city : str or int a list of them, default None
        Codes of the cities to be selected.

    state : str or int or a list of them, default None
        Codes of the states to be selected.

    macroregion : str or int or a list of them, default None
        Codes of the macroregions to be selected.

    microregion : str or int or a list of them, default None
        Codes of the microregion to be selected.

    mesoregion : str or int or a list of them, default None
        Codes of the mesoregions to be selected.

    classifications : dict, int, str or list, default None
        { classification : [categories], ... }
        classification1
        "classification1"
        list = [classification1, classification2, ... ]

    Returns
    -------
    A DataFrame with series values and metadata.
    """
    baseurl = f"https://servicodados.ibge.gov.br/api/v3/agregados/{code}"
    # handle dates part of url
    frequency = get_frequency(code)
    dates = ibge_build_dates_query(start, end, last_n, frequency)
    # handle variables, locations and classifications part of url
    variables = ibge_build_variables_query(variables)
    locations = ibge_build_location_query(city, state, macroregion, microregion, mesoregion, brazil)
    classifications = ibge_build_classification_query(classifications)
    url = f"{baseurl}{dates}{variables}?{classifications}{locations}&view=flat"
    return parse_ibge_response(url)

## Get metadata


def get_frequency(aggregate_code):
    return list_periods(aggregate_code).loc["frequency", :].values


def get_metadata(aggregate_code):
    url = f"https://servicodados.ibge.gov.br/api/v3/agregados/{aggregate_code}/metadados"
    json = get_json(url)
    return pd.DataFrame.from_dict(json, orient="index", columns=["values"])

## List Metadata Functions


def search(*search, **searches):
    """
    Function to list all aggregated variables of IBGE.

    Parameters
    ----------
    search : str
        Strings to search.

    where : str, default "nome"
        Where to search.

    Returns
    -------
    A DataFrame with metadata about the aggregates.
    """
    json = get_json("https://servicodados.ibge.gov.br/api/v3/agregados")
    df = pd.io.json.json_normalize(
        json, record_path="agregados", meta=["id", "nome"], meta_prefix="pesquisa_"
    )
    if search or searches:
        return do_search(df, search, searches)
    return df


def list_variables(aggregate_code, *search, **searches):
    """
    Function to list all variables associated with an aggregate of IBGE.

    Parameters
    ----------
    search : str
        Strings to search.

    where : str, default "nome"
        Where to search.

    Returns
    -------
    A DataFrame with metadata about the variables.
    """
    baseurl = "https://servicodados.ibge.gov.br/api/v3"
    query = f"/agregados/{aggregate_code}/variaveis/all?localidades=BR"
    url = f"{baseurl}{query}"
    json = get_json(url)
    df = pd.io.json.json_normalize(json).iloc[:, :3]
    if search or searches:
        return do_search(df, search, searches)
    return df


def list_locations(aggregate_code):
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
    codes = get_json(url)["nivelTerritorial"]["Administrativo"]
    df = pd.DataFrame({"codes": codes})
    df["parameters"] = [locations_dict.get(code) for code in df.codes]
    return df


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


def list_classifications(aggregate_code, *search, **searches):
    """
    Function to list all classification of a given aggregate.

    Parameters
    ----------
    search : str
        Strings to search.

    where : str, default "nome"
        Where to search.

    Returns
    -------
    A DataFrame with the classifications and their categories.
    """
    baseurl = "https://servicodados.ibge.gov.br/api/v3/agregados"
    url = f"{baseurl}/{aggregate_code}/metadados"
    json = get_json(url)
    classifications = json["classificacoes"]
    df = pd.io.json.json_normalize(
        classifications,
        "categorias",
        meta=["id", "nome"],
        meta_prefix="classificacao_"
    )
    if search or searches:
        return do_search(df, search, searches)
    return df


def list_states(*search, **searches):
    """
    Function to list all states and their codes.

    Parameters
    ----------
    search : str
        Strings to search.

    where : str, default "nome"
        Where to search.

    Returns
    -------
    A DataFrame with metadata about the states.
    """
    return list_regions("estados", search, searches)


def list_macroregions(*search, **searches):
    """
    Function to list all macroregions and their codes.

    Parameters
    ----------
    search : str
        Strings to search.

    where : str, default "nome"
        Where to search.

    Returns
    -------
    A DataFrame with metadata about the about the states.
    """
    return list_regions("regioes", search, searches)


def list_cities(*search, **searches):
    """
    Function to list all cities and their codes.

    Parameters
    ----------
    search : str
        Strings to search.

    where : str, default "nome"
        Where to search.

    Returns
    -------
    A DataFrame with metadata about the cities.
    """
    return list_regions("municipios", search, searches)


def list_microregions(*search, **searches):
    """
    Function to list all microregions.

    Parameters
    ----------
    search : str
        Strings to search.

    where : str, default "nome"
        Where to search.

    Returns
    -------
    A DataFrame with metadata about the microregions.
    """
    return list_regions("microrregioes", search, searches)


def list_mesoregions(*search, **searches):
    """
    Function to list all mesoregions and their codes.

    Parameters
    ----------
    search : str
        Strings to search.

    where : str, default "nome"
        Where to search.

    Returns
    -------
    A DataFrame with metadata about the mesoregions.
    """
    return list_regions("mesorregioes", search, searches)

# vi: nowrap
