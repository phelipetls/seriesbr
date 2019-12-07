from pandas import concat, DataFrame
from .helpers.utils import return_codes_and_names
from .helpers.lists import list_metadata, ipea_metadata_list
from .helpers.response import parse_ipea_response
from .helpers.searching import return_search_results_ipea
from .helpers.request import get_json
from .helpers.dates import parse_dates
from .helpers.url import (
    ipea_make_select_query,
    ipea_make_filter_query,
)


def get_serie(code, name=None, start=None, end=None):
    """
    Returns a time series from IPEADATA database.

    Parameters
    ----------
    code : int or str
        The code of the time series.

    name : str
        The name of the series.

    start : str
        Initial date, year last.

    end : str
        End date, year last.

    Returns
    -------
    pandas.DataFrame
    """
    assert isinstance(code, str), "Not a valid code format."
    baseurl = "http://ipeadata2-homologa.ipea.gov.br/api/v1/"
    resource_path = f"ValoresSerie(SERCODIGO='{code}')"
    select = "?$select=VALDATA,VALVALOR"
    start, end = parse_dates(start, end, api="ipeadata")
    dates = date_filter(start, end)
    url = f"{baseurl}{resource_path}{select}{dates}"
    serie = parse_ipea_response(url, code, name)
    return serie


def date_filter(start, end):
    """
    Auxiliary function to return the right query
    to filter dates.
    """
    if start and end:
        data = f"&$filter=VALDATA ge {start} and VALDATA le {end}"
    elif start:
        data = f"&$filter=VALDATA ge {start}"
    elif end:
        data = f"&$filter=VALDATA le {end}"
    else:
        data = ""
    return data


def get_series(*codes, start=None, end=None, **kwargs):
    """
    Get multiple series all at once in a single data frame.

    Parameters
    ----------
    codes : dict, str, int
        Dictionary like {"name1": cod1, "name2": cod2}
        or a bunch of code numbers like cod1, cod2.

    start : str
        Initial date.

    end : str
        End date.

    **kwargs
        Arguments to pandas.concat.

    Returns
    -------
    pandas.DataFrame with the requested series.
    """
    assert codes, "You must pass at least one code to be searched."
    codes, names = return_codes_and_names(*codes)
    return concat(
        (get_serie(code, name, start, end) for code, name in zip(codes, names)),
        axis="columns",
        sort=True,
        **kwargs,
    )


def search(SERNOME="", **fields):
    baseurl = "http://ipeadata2-homologa.ipea.gov.br/api/v1/"
    resource_path = "Metadados"
    select_query = ipea_make_select_query(fields)
    filter_query = ipea_make_filter_query(SERNOME, fields)
    url = f"{baseurl}{resource_path}{select_query}{filter_query}"
    results = return_search_results_ipea(url)
    return results


def get_metadata(code):
    """
    Returns metadata of a series specified by the a code.
    """
    baseurl = "http://ipeadata2-homologa.ipea.gov.br/api/v1/"
    resource_path = f"Metadados('{code}')"
    url = f"{baseurl}{resource_path}"
    results = get_json(url)
    return DataFrame.from_dict(results["value"][0], orient="index", columns=["values"])


def list_themes():
    """
    List all themes available in the database.
    """
    return list_metadata("Temas")


def list_countries():
    """
    List all countries available in the database.
    """
    return list_metadata("Paises")


def list_fields():
    """
    Pretty print dictionary of metadata with their description as values
    """
    return DataFrame.from_dict(ipea_metadata_list, orient='index', columns=["Descrição"])
