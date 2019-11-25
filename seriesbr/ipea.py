from pandas import concat
from .helpers.types import check_cods
from .helpers.request import custom_get
from .helpers.response import parse_response
from .helpers.formatter import format_search_ipea, to_table
from .helpers.dates import parse_dates
from .helpers.metadata import make_select_query, make_filter_query
# MANUAL: http://ipeadata.gov.br/api/


def get_serie(cod, start=None, end=None, name=None, out="pd"):
    """
    Returns a time series from IPEADATA database.

    Parameters:
    cod (int or str): The code of the time series.

    name (str): The name of the series.

    start (str): Initial date.

    end (str): End date.

    out (str): Output format (either "pd" or "raw")

    Returns:
    str: if out == "raw"
    pandas.DataFrame: if out == "pd"
    """
    baseurl = "http://ipeadata2-homologa.ipea.gov.br/api/v1/"
    resource_path = f"ValoresSerie(SERCODIGO='{cod}')"
    select = "?$select=VALDATA,VALVALOR"
    start, end = parse_dates(start, end, api="ipeadata")
    dates = date_filter(start, end)
    url = f"{baseurl}{resource_path}{select}{dates}"
    serie = parse_response(custom_get(url), cod, name, out, source="ipea")
    return serie


def date_filter(start, end):
    """
    Auxiliary function to return the right query
    to filter dates.

    """
    # TODO: Yes, this is ugly. Got to improve this.
    if start and end:
        data = f"&$filter=VALDATA ge {start} and VALDATA le {end}"
    elif start:
        data = f"&$filter=VALDATA ge {start}"
    elif end:
        data = f"&$filter=VALDATA le {end}"
    else:
        data = ""
    return data


def get_series(*cods, start=None, end=None, **kwargs):
    """
    Get multiple series all at once in a single data frame.

    Parameters:
    cods (dict, str, int): dictionary like {"name1": cod1, "name2": cod2}
    or a bunch of code numbers like cod1, cod2.

    start (str): Initial date.

    end (str): End date.

    **kwargs: passed to pandas.concat.

    Returns:
    pandas.DataFrame with the requested series.
    """
    codes, names = check_cods(*cods)
    # TODO: maybe I should make a function fot this... not straight-forward.
    return concat(
        [get_serie(cod, start, end) for cod in codes],
        axis="columns",
        sort=True,  # done to avoid pandas warning messages
        **kwargs,
    ).rename(columns={cod: name for name, cod in zip(names, codes)})


def search(**kwargs):
    baseurl = "http://ipeadata2-homologa.ipea.gov.br/api/v1/"
    resource_path = "Metadados"
    select_query = make_select_query(kwargs)
    filter_query = make_filter_query(kwargs)
    url = f"{baseurl}{resource_path}{select_query}{filter_query}"
    print(url)
    results = custom_get(url).json()["value"]
    format_search_ipea(results)


def get_metadata(cod):
    """
    Returns metadata of a series specified by cod.
    """
    baseurl = "http://ipeadata2-homologa.ipea.gov.br/api/v1/"
    resource_path = f"Metadados('{cod}')"
    url = f"{baseurl}{resource_path}"
    metadados = custom_get(url).json()["value"][0]
    to_table(metadados.keys(), metadados.values())
