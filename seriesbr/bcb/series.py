import pandas as pd

from seriesbr.utils import session, misc, dates
from datetime import datetime

DATE_FORMAT = "%d/%m/%Y"


def get_series(*args, start=None, end=None, last_n=None, **kwargs):
    """
    Get multiple BCB time series.

    Parameters
    ----------

    *args : int, dict
        Arbitrary number of time series codes.

    start : str, optional
        Initial date.

    end : str, optional
        Final date.

    last_n : int, optional
        Number of last observations.

    **kwargs
        Passed to pandas.concat

    Returns
    -------
    pandas.DataFrame
    """
    parsed_args = misc.parse_arguments(*args)

    def get_timeseries(code, label=None, start=None, end=None, last_n=None):
        url, params = build_url(code, start, end, last_n)
        response = session.get(url, params=params)
        json = response.json()
        return build_df(json, code, label)

    return pd.concat(
        (
            get_timeseries(code, label, start=start, end=end, last_n=last_n)
            for label, code in parsed_args.items()
        ),
        axis="columns",
        sort=True,
        **kwargs,
    )


def build_url(code, start=None, end=None, last_n=None):
    assert isinstance(code, (str, int)), "Not a valid code format."

    url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{code}/dados"
    params = {"format": "json"}

    if last_n:
        url += f"/ultimos/{last_n}"
        return url, params

    if not start and not end:
        return url, params

    start = dates.parse_start_date(start) if start else dates.UNIX_EPOCH
    params["dataInicial"] = start.strftime(DATE_FORMAT)

    end = dates.parse_end_date(end) if end else datetime.today()
    params["dataFinal"] = end.strftime(DATE_FORMAT)

    return url, params


def build_df(json, code, label):
    df = pd.DataFrame(json)

    df["valor"] = df["valor"].astype("float64")

    df = df.set_index("data")
    df = df.rename_axis("Date")
    df.index = pd.to_datetime(df.index, format="%d/%m/%Y")

    df.columns = [label or code]

    return df
