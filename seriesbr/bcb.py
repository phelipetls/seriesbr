from pandas import concat
from .helpers.dates import parse_dates
from .helpers.types import check_cods
from .helpers.response import parse_response
from .helpers.request import custom_get
from .helpers.formatter import format_response_bcb


def get_serie(cod, start=None, end=None, name=None, last_n=None, out="pd"):
    """
    Returns a time series from Time Series Management System (SGS)
    of Brazilian Central Bank (BCB).

    Parameters:
    cod (int or str): The code of the time series.

    name (str): The name of the series.

    start (str): Initial date.

    end (str): End date.

    last_n (int): Ignore other arguments and get the last
    n observations.

    out (str): Output format (either "pd" or "json")

    Returns:
    str: if out == "raw"
    pandas.DataFrame: if out == "pd"
    """
    baseurl = f"http://api.bcb.gov.br/dados/serie/bcdata.sgs.{cod}/dados"
    formato = "?formato=json"
    if last_n:
        url = f"{baseurl}/ultimos/{last_n + 1}?formato=json"
    else:
        start, end = parse_dates(start, end, api="bcb")
        dates = f"&dataInicial={start}&dataFinal={end}"
        url = f"{baseurl}{formato}{dates}"
    return parse_response(custom_get(url), cod, name, out, source="bcb")


def get_series(*cods, start=None, end=None, last_n=None, join="outer", **kwargs):
    """
    Get multiple series all at once in a single data frame.

    Parameters:
    cods (dict, str, int): dictionary like {"name1": cod1, "name2": cod2}
    or a bunch of code numbers like cod1, cod2.

    start (str): Initial date.

    end (str): End date.

    last_n (int): Get last_n observations.

    join (str): "outer" givess all observations and
    "inner" gives the intersection of them.

    **kwargs: passed to pandas.concat.

    Returns:
    pandas.DataFrame with the series
    """
    codes, names = check_cods(*cods)
    return concat(
        [get_serie(cod, start, end, last_n) for cod in codes],
        axis="columns",
        join=join,
        **kwargs
    ).rename(columns={cod: nome for nome, cod in zip(names, codes)})


def search(name, rows=10, page=1):
    """
    Search for a name in the SGS database.

    Parameters:
    name (str): string to search.

    rows (int or str): how many results to show.

    page (int or str): page of results.

    Returns:
    None. Just prints the search results.
    """
    url = "https://dadosabertos.bcb.gov.br/api/3/action/package_search?"
    params = {"q": name, "rows": rows, "start": page * rows, "sort": "relevance asc"}
    response = custom_get(url, params=params)
    format_response_bcb(response)
