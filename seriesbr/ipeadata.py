from pandas import concat
from .helpers.types import check_cods
from .helpers.request import custom_get
from .helpers.response import parse_response
from .helpers.formatter import format_search_ipea, to_table
from .helpers.dates import parse_dates
from .helpers.metadata import make_select_query, make_filter_query


def get(cod, start=None, end=None, name=None, out="pd"):
    """
    Returns a time series from IPEADATA 3.0 database.

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
    select = "?$select=VALDATA,VALVALOR"  # just return the date and values
    # TODO: query dates (very hard with OData apparently)
    url = f"{baseurl}{resource_path}{select}"
    serie = parse_response(custom_get(url), cod, name, out, source="ipea")
    if out == "pd":
        if start and end:
            return serie[start:end]
        elif start:
            return serie[start:]
        elif end:
            return serie[:end]
        else:
            return serie
    return serie


def get_series(*cods, start=None, end=None, last_n=None, join="outer", **kwargs):
    """
    Get multiple series all at once in a single data frame.

    Parameters:
    cods (dict, str, int): dictionary like {"name1": cod1, "name2": cod2}
    or a bunch of code numbers like cod1, cod2.

    start (str): Initial date.

    end (str): End date.

    join (str): "outer" givess all observations and
    "inner" gives the intersection of them.

    **kwargs: passed to pandas.concat.

    Returns:
    pandas.DataFrame with the series
    """
    codes, names = parse_cods(*cods)
    return concat(
        [get(cod, start, end) for cod in codes],
        axis="columns",
        join=join,
        sort=True,  # done to avoid pandas warning messages
        **kwargs
    ).rename(columns={cod: name for name, cod in zip(names, codes)})


def search(name):
    """
    Search for a name in the IPEADATA database.

    Parameters:
    name (str): string to search.

    Returns:
    None. Just prints the search results.
    """
    baseurl = "http://ipeadata2-homologa.ipea.gov.br/api/v1/"
    resource_path = "Metadados"
    query = f"?$select=SERCODIGO,SERNOME&$filter=contains(SERNOME,'{name}')"
    url = f"{baseurl}{resource_path}{query}"
    results = custom_get(url).json()["value"]
    format_results_ipea(results)
