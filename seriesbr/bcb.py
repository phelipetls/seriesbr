from pandas import concat
from .helpers.dates import parse_dates
from .helpers.types import check_and_return_codes_and_names
from .helpers.response import parse_response
from .helpers.request import custom_get
from .helpers.search_results import return_search_results_bcb


def get_serie(code, start=None, end=None, name=None, last_n=None):
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
    baseurl = f"http://api.bcb.gov.br/dados/serie/bcdata.sgs.{code}/dados?formato=json"
    if last_n:
        url = f"{baseurl}/ultimos/{last_n + 1}?formato=json"
    else:
        start, end = parse_dates(start, end, api="bcb")
        dates = f"&dataInicial={start}&dataFinal={end}"
        url = f"{baseurl}{dates}"
    return parse_response(custom_get(url), code, name, source="bcb")


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
    codes, names = check_and_return_codes_and_names(*codes)
    return concat(
        [get_serie(cod, start, end, last_n) for cod in codes],
        axis="columns",
        join=join,
        **kwargs
    ).rename(columns={cod: nome for nome, cod in zip(names, codes)})


def search(name="", *filters, rows=10, start=1):
    """
    Search for a name in the SGS database.

    Parameters
    ----------
    name (str): string to search.

    rows (int or str): how many results to show.

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
    params = f"q={name}&rows={rows}&start={start}&sort=score desc"
    filter_params = "+".join(f"{value}" for value in filters if filters)
    url = f"{baseurl}{params}{'&fq=' if filters else ''}{filter_params}"
    response = custom_get(url)
    count, results = return_search_results_bcb(response)
    search_message = f"{rows if rows < count else count} out of {count} results, starting at row {start}"
    print(search_message)
    return results



    Returns:
    None. Just prints the search results.
    """
    url = "https://dadosabertos.bcb.gov.br/api/3/action/package_search?"
    params = {"q": name, "rows": rows, "start": page * rows, "sort": "relevance asc"}
    response = custom_get(url, params=params)
    format_response_bcb(response)
