from pandas import concat, DataFrame
from pprint import pprint
from .helpers.types import return_codes_and_names
from .helpers.request import custom_get
from .helpers.response import parse_response
from .helpers.search_results import return_search_results_ipea
from .helpers.dates import parse_dates
from .helpers.metadata import (
    ipea_make_select_query,
    ipea_make_filter_query,
    ipea_metadata_list,
)


def get_serie(code, name=None, start=None, end=None):
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
    assert isinstance(code, str), "Not a valid code format."
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
    assert codes, "You must pass at least one code to be searched."
    codes, names = return_codes_and_names(*codes)
    return concat(
        [get_serie(code, name, start, end) for code, name in zip(codes, names)],
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


def list_themes():
    """
    List all themes available.
    """
    return DataFrame(list_metadata("Temas", "TEMCODIGO", "TEMNOME"))


def list_countries():
    """
    List all countries available
    """
    return DataFrame(list_metadata("Paises", "PAICODIGO", "PAINOME"))


def list_metadata(resource_path, code_key, value_key):
    baseurl = "http://www.ipeadata.gov.br/api/odata4/"
    url = f"{baseurl}{resource_path}"
    response = custom_get(url).json()["value"]
    return [{code_key: item[code_key], value_key: item[value_key]} for item in response]


def list_fields():
    """
    Pretty print dictionary of metadata with their description as values
    """
    pprint(ipea_metadata_list)
