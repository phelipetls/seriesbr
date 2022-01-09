import pandas as pd
from seriesbr.utils import session, misc, dates

DATE_FORMAT = "%Y-%m-%dT00:00:00Z"


def get_series(*args, start=None, end=None, **kwargs):
    """
    Get multiple IPEA time series.

    Parameters
    ----------

    *args : int, dict
        Arbitrary number of time series codes.

    start : str, optional
        Initial date.

    end : str, optional
        Final date.

    **kwargs
        Passed to pandas.concat

    Returns
    -------
    pandas.DataFrame
    """
    parsed_args = misc.parse_arguments(*args)

    def get_timeseries(code, label=None, start=None, end=None):
        url, params = build_url(code, start, end)
        response = session.get(url, params=params)
        json = response.json()
        df = build_df(json, code, label)
        return df

    return pd.concat(
        (
            get_timeseries(code, label, start=start, end=end)
            for label, code in parsed_args.items()
        ),
        axis="columns",
        sort=True,
        **kwargs,
    )


def build_df(json, code, label):
    json = json["value"]
    df = pd.DataFrame(json)

    df["VALDATA"] = df["VALDATA"].str[:-6]
    df = df.set_index("VALDATA")
    df = df.rename_axis("Date")
    df.index = pd.to_datetime(df.index, format="%Y-%m-%dT%H:%M:%S")

    df["VALVALOR"] = pd.to_numeric(df["VALVALOR"], errors="coerce")
    df.columns = [label or code]

    return df


def build_url(code, start, end):
    assert isinstance(code, str), "Not a valid code format."

    params = {"$select": "VALDATA,VALVALOR"}

    url = (
        f"http://ipeadata2-homologa.ipea.gov.br/api/v1/ValoresSerie(SERCODIGO='{code}')"
    )

    if start:
        start = dates.parse_start_date(start).strftime(DATE_FORMAT)

    if end:
        end = dates.parse_end_date(end).strftime(DATE_FORMAT)

    date_filter = ipea_filter_by_date(start, end)
    if date_filter:
        params["$filter"] = date_filter

    return url, params


def ipea_filter_by_date(start=None, end=None):
    """
    Filter an IPEA time series by date.

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
    >>> url.ipea_filter_by_date("2019-01-01T00:00:00-00:00", "2019-02-01T00:00:00-00:00")
    'VALDATA ge 2019-01-01T00:00:00-00:00 and VALDATA le 2019-02-01T00:00:00-00:00'
    """

    def filter_by_start_date(start):
        return f"VALDATA ge {start}"

    def filter_by_end_date(start):
        return f"VALDATA le {start}"

    if start and end:
        return filter_by_start_date(start) + " and " + filter_by_end_date(end)
    elif start:
        return filter_by_start_date(start)
    elif end:
        return filter_by_end_date(end)

    return ""
