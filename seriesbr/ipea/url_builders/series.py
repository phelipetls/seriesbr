from seriesbr.utils import dates


def build_url(code, start, end):
    assert isinstance(code, str), "Not a valid code format."

    url = "http://ipeadata2-homologa.ipea.gov.br/api/v1/"
    url += f"ValoresSerie(SERCODIGO='{code}')"
    url += "?$select=VALDATA,VALVALOR"

    start, end = dates.parse_dates(start, end, api="ipea")
    url += ipea_filter_by_date(start, end)

    return url


def ipea_filter_by_date(start=None, end=None):
    """
    Help filter an IPEA time series by date.

    Parameters
    ----------
    start : str
        Start date string.

    End : str
        End date string.

    Returns
    -------
    str
        A string to filter by dates.

    Examples
    --------
    >>> url.ipea_make_dates_query("2019-01-01T00:00:00-00:00", "2019-02-01T00:00:00-00:00")
    '&$filter=VALDATA ge 2019-01-01T00:00:00-00:00 and VALDATA le 2019-02-01T00:00:00-00:00'
    """
    dates = ""

    if start and end:
        dates = f"&$filter=VALDATA ge {start} and VALDATA le {end}"
    elif start:
        dates = f"&$filter=VALDATA ge {start}"
    elif end:
        dates = f"&$filter=VALDATA le {end}"

    return dates
