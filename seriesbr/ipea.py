from pandas import concat
from .helpers.types import expect_type
from .helpers.request import custom_get
from .helpers.response import parse_response
from .helpers.search_results import return_search_results_ipea
from .helpers.dates import parse_dates
from .helpers.metadata import (
    ipea_make_select_query,
    ipea_make_filter_query,
    print_suggestions,
)


def get_serie(code, start=None, end=None, name=None):
    """
    Returns a time series from IPEADATA database.

    Parameters
    ----------
    code (int or str): The code of the time series.

    name (str): The name of the series.

    start (str): Initial date.

    end (str): End date.

    Returns
    -------
    pandas.DataFrame
    """
    baseurl = "http://ipeadata2-homologa.ipea.gov.br/api/v1/"
    resource_path = f"ValoresSerie(SERCODIGO='{code}')"
    select = "?$select=VALDATA,VALVALOR"
    start, end = parse_dates(start, end, api="ipeadata")
    dates = date_filter(start, end)
    url = f"{baseurl}{resource_path}{select}{dates}"
    serie = parse_response(custom_get(url), code, name, source="ipea")
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
    codes (dict, str, int): dictionary like {"name1": cod1, "name2": cod2}
    or a bunch of code numbers like cod1, cod2.

    start (str): Initial date.

    end (str): End date.

    **kwargs: passed to pandas.concat.

    Returns
    -------
    pandas.DataFrame with the requested series.
    """
    codes, names = expect_type(*codes)
    return concat(
        [get_serie(code, start, end) for code in codes],
        axis="columns",
        **kwargs,
    ).rename(columns={code: name for name, code in zip(names, codes)})


def search(SERNOME="", **fields):
    baseurl = "http://ipeadata2-homologa.ipea.gov.br/api/v1/"
    resource_path = "Metadados"
    select_query = ipea_make_select_query(fields)
    filter_query = ipea_make_filter_query(SERNOME, fields)
    url = f"{baseurl}{resource_path}{select_query}{filter_query}"
    print(url)
    response = custom_get(url)
    results = return_search_results_ipea(response)
    return results


def get_metadata(cod):
    """
    Returns metadata of a series specified by cod.
    """
    baseurl = "http://ipeadata2-homologa.ipea.gov.br/api/v1/"
    resource_path = f"Metadados('{cod}')"
    url = f"{baseurl}{resource_path}"
    results = custom_get(url).json()["value"][0]
    return results

def get_suggestions():
    print_suggestions()
