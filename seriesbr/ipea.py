from pandas import concat, DataFrame
from .helpers.dates import parse_dates
from .helpers.utils import return_codes_and_names
from .helpers.lists import list_metadata_helper
from .helpers.request import get_json
from .helpers.response import ipea_json_to_df
from .helpers.searching import get_search_results_ipea
from .helpers.ipea_metadata_list import ipea_metadata_list
from .helpers.url import (
    ipea_make_select_query,
    ipea_make_filter_query,
    ipea_make_dates_query,
)


def get_serie(code, name=None, start=None, end=None):
    """
    Auxiliary function to return a single time series
    from IPEA database.
    """
    assert isinstance(code, str), "Not a valid code format."
    baseurl = "http://ipeadata2-homologa.ipea.gov.br/api/v1/"
    resource_path = f"ValoresSerie(SERCODIGO='{code}')"
    select = "?$select=VALDATA,VALVALOR"
    start, end = parse_dates(start, end, api="ipeadata")
    dates = ipea_make_dates_query(start, end)
    url = f"{baseurl}{resource_path}{select}{dates}"
    json = get_json(url)
    return ipea_json_to_df(json, code, name)


def get_series(*codes, start=None, end=None, **kwargs):
    """
    Get multiple series all at once in a single data frame.

    Parameters
    ----------
    codes : dict, str, int
        Dictionary like {"name1": cod1, "name2": cod2}
        or a bunch of code numbers, e.g. cod1, cod2.

    start : str
        Initial date, month or day first.

    end : str
        End date, month or day first.

    **kwargs
        Passed to pandas.concat.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with series' values.
    """
    codes, names = return_codes_and_names(*codes)
    return concat(
        (get_serie(code, name, start, end) for code, name in zip(codes, names)),
        axis="columns",
        sort=True,
        **kwargs,
    )


def search(*SERNOME, **metadatas):
    """
    Function to search in IPEA's database.

    Parameters
    ----------
    *SERNOME
        String(s) to look up for in a series' name.

    **metadatas
        Keyword arguments where parameter is a valid metadata
        and value a str or list of str.
    """
    baseurl = "http://ipeadata2-homologa.ipea.gov.br/api/v1/"
    resource_path = "Metadados"
    select_query = ipea_make_select_query(metadatas)
    filter_query = ipea_make_filter_query(SERNOME, metadatas)
    url = f"{baseurl}{resource_path}{select_query}{filter_query}"
    return get_search_results_ipea(url)


def get_metadata(code):
    """
    Get metadata of a series specified by the a code.

    Parameters
    ----------
    code : int or str

    Returns
    -------
    pandas.DataFrame
        A DataFrame with the series' metadata.
    """
    baseurl = "http://ipeadata2-homologa.ipea.gov.br/api/v1/"
    resource_path = f"Metadados('{code}')"
    url = f"{baseurl}{resource_path}"
    results = get_json(url)
    return DataFrame.from_dict(results["value"][0], orient="index", columns=["values"])


def list_themes():
    """
    Function to list all themes available in the database.
    """
    return list_metadata_helper("Temas")


def list_countries():
    """
    Function to list all countries available in the database.
    """
    return list_metadata_helper("Paises")


def list_metadata():
    """
    Function to list all valid metadatas.
    """
    return DataFrame.from_dict(ipea_metadata_list, orient='index', columns=["Description"])
