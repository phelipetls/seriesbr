from pandas import concat, DataFrame
from .helpers.dates import parse_dates
from .helpers.utils import return_codes_and_names
from .helpers.response import parse_bcb_response
from .helpers.request import get_json
from .helpers.searching import return_search_results_bcb


def get_serie(code, name=None, start=None, end=None, last_n=None):
    """
    Returns a time series from Time Series Management System (SGS)
    of Brazilian Central Bank (BCB).

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

    last_n : inr
    Ignore other arguments and get the last n observations.

    Returns
    -------
    pandas.DataFrame
    """
    assert isinstance(code, str) or isinstance(code, int), "Not a valid code format."
    baseurl = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{code}/dados"
    if last_n:
        url = f"{baseurl}/ultimos/{last_n}?formato=json"
    else:
        start, end = parse_dates(start, end, api="bcb")
        dates = f"&dataInicial={start}" if start else start
        dates += f"&dataFinal={end}" if end else end
        url = f"{baseurl}?format=json{dates}"
    return parse_bcb_response(url, code, name)


def get_series(*codes, start=None, end=None, last_n=None, **kwargs):
    """
    Get multiple series all at once in a single data frame.

    Parameters
    ----------
    codes : dict, str, int
        Dictionary like {"name1": cod1, "name2": cod2} or a bunch of code numbers like cod1, cod2.

    start : str
        Initial date.

    end : str
        End date.

    last_n : int
        Get last_n observations.

    **kwargs
        Passed to pandas.concat.

    Returns
    -------
    A DataFrame with the series.
    """
    assert codes, "You must pass at least one code."
    codes, names = return_codes_and_names(*codes)
    return concat(
        (get_serie(code, name, start, end, last_n)
         for code, name in zip(codes, names)),
        axis="columns",
        sort=True,
        **kwargs
    )


def search(name="", *filters, rows=10, skip=1):
    """
    Search for a name in the SGS database.

    Parameters
    ----------
    name : str
        String to search.

    skip : int or str
        How many results to show.

    start : int or str
        Start showing from this result.

    Returns
    -------
    A DataFrame with the results.
    """
    baseurl = "https://dadosabertos.bcb.gov.br/api/3/action/package_search?"
    params = f"q={name}&rows={rows}&start={skip}&sort=score desc"
    filter_params = f"&fq={'+'.join([value for value in filters])}" if filters else ""
    url = f"{baseurl}{params}{filter_params}"
    results = return_search_results_bcb(url)
    return results


def get_metadata(code):
    """
    Get metadata of a series given its code.

    Parameters
    ----------
    code : str
        Code to search.

    Returns
    -------
    A dictionary with the results.
    """
    baseurl = "https://dadosabertos.bcb.gov.br/api/3/action/package_search?"
    params = f"fq=codigo_sgs:{code}"
    url = f"{baseurl}{params}"
    results = get_json(url)["result"]["results"]
    return DataFrame.from_dict(results[0], orient="index", columns=["values"])
