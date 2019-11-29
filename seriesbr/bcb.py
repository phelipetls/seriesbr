from pandas import concat
from .helpers.dates import parse_dates
from .helpers.types import return_codes_and_names
from .helpers.response import parse_response
from .helpers.request import custom_get
from .helpers.search_results import return_search_results_bcb


def get_serie(code, name=None, start=None, end=None, last_n=None):
    """
    Returns a time series from Time Series Management System (SGS)
    of Brazilian Central Bank (BCB).

    Parameters
    ----------
    code (int or str): The code of the time series.

    name (str): The name of the series.

    start (str): Initial date.

    end (str): End date.

    last_n (int): Ignore other arguments and get the last
    n observations.

    Returns
    -------
    pandas.DataFrame
    """
    assert isinstance(code, str) or isinstance(code, int), "Not a valid code format."
    baseurl = f"http://api.bcb.gov.br/dados/serie/bcdata.sgs.{code}/dados"
    if last_n:
        url = f"{baseurl}/ultimos/{last_n - 1}?formato=json"
    else:
        start, end = parse_dates(start, end, api="bcb")
        dates = f"&dataInicial={start}&dataFinal={end}"
        url = f"{baseurl}?format=json{dates}"
    return parse_response(custom_get(url), code, name, source="bcb")


def get_series(*codes, start=None, end=None, last_n=None, **kwargs):
    """
    Get multiple series all at once in a single data frame.

    Parameters
    ----------
    codes (dict, str, int): dictionary like {"name1": cod1, "name2": cod2}
    or a bunch of code numbers like cod1, cod2.

    start (str): Initial date.

    end (str): End date.

    last_n (int): Get last_n observations.

    join (str): "outer" givess all observations and
    "inner" gives the intersection of them.

    **kwargs: passed to pandas.concat.

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
    name (str): string to search.

    skip (int or str): how many results to show.

    start (int or str): start showing from this result.

    Returns
    -------
    A DataFrame with the results.
    """
    # The api also takes parameters (filter queries)
    # but very often it returned nothing.
    # It turned out that, when I tried withou specifying
    # the queried parameters, I got better results in general
    # so I've sticked with this.
    # It doens't accept any keyword arguments, just positional arguments
    # that are then joined and passed to the &fq= API parameter.
    baseurl = "https://dadosabertos.bcb.gov.br/api/3/action/package_search?"
    params = f"q={name}&rows={rows}&start={skip}&sort=score desc"
    filter_params = "&fq=" + "+".join(f"{value}" for value in filters if filters)
    url = f"{baseurl}{params}{filter_params}"
    response = custom_get(url)
    results = return_search_results_bcb(response)
    return results


def get_metadata(code):
    """
    Get metadata of a series given its code.

    Parameters
    ----------
    code (str): code to search.

    Returns
    -------
    A dictionary with the results.
    """
    baseurl = "https://dadosabertos.bcb.gov.br/api/3/action/package_search?"
    params = f"fq=codigo_sgs:{code}"
    url = f"{baseurl}{params}"
    results = custom_get(url).json()["result"]["results"][0]
    return results
