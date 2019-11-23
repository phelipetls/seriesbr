from pandas import concat
from helpers.dates import parse_date
from helpers.types import parse_cods
from helpers.response import parse_response
from helpers.request import get_serie


def get(cod, name=None, start=None, end=None, last_n=None, out="pd"):
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

    out (str): Output format (either "pd" or "raw")

    Returns:
    str: if out == "raw"
    pandas.DataFrame: if out == "pd"
    """
    base_url = f"http://api.bcb.gov.br/dados/serie/bcdata.sgs.{cod}/dados"
    formato = "?formato=json"
    if last_n:
        url = base_url + f"/ultimos/{last_n + 1}?formato=json"
    else:
        data = parse_dates(start, end)
        url = base_url + formato + data
    return parse_response(custom_get(url).text, cod, name, out, source="bcb")


def parse_dates(start, end):
    """
    Auxiliary function to convert different date formats
    to %d/%m/%Y, required by the SGS API.
    """
    start = parse_date(start, start=True) if start else start
    end = parse_date(end, start=False) if end else end
    if start and end:
        data = f"&dataInicial={start}&dataFinal={end}"
    elif start:
        data = f"&dataInicial={start}"
    elif end:
        data = f"&dataFinal={end}"
    else:
        data = ""
    return data


def get_series(*cods, start=None, end=None, last_n=None, join="outer", **kwargs):
    """
    Get multiple series all at once in a single data frame.

    Parameters:
    cods (dict, str, int): dictionary like {"name1": cod1, "name2": cod2}
    or a bunch of code numbers like cod1, cod2.

    start (str): Initial date.

    end (str): End date.

    last_n (int): Get last n observations.

    join (str): "outer" givess all observations and
    "inner" gives the intersection of them.

    **kwargs: passed to pandas.concat.

    Returns:
    pandas.DataFrame with the series
    """
    codes, names = parse_cods(*cods)
    return concat(
        [get(cod, start, end, last_n) for cod in codes],
        axis="columns",
        join=join,
        **kwargs
    ).rename(columns={cod: nome for nome, cod in zip(names, codes)})


