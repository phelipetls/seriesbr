import pandas as pd

from datetime import datetime
from .metadata import get_metadata, IpeaMetadata
from seriesbr.utils import session, dates
from dateutil.relativedelta import relativedelta
from typing import Tuple, TypedDict, Optional


def get_series(
    code: str,
    start: str = None,
    end: str = None,
    last_n: int = None,
) -> pd.DataFrame:
    """
    Get multiple IPEA time series.

    Parameters
    ----------

    code : str
        Series identifier.

    start : str, optional
        Initial date.

    end : str, optional
        Final date.

    Returns
    -------
    pandas.DataFrame
    """

    metadata = get_metadata(code)
    url, params = build_url(code, start, end, last_n, metadata)

    response = session.get(url, params=params)
    json = response.json()

    df = build_df(json, code)
    return df


def build_df(json: dict, code: str) -> pd.DataFrame:
    json = json["value"]
    df = pd.DataFrame(json)

    df["VALDATA"] = df["VALDATA"].str[:-6]
    df["VALDATA"] = pd.to_datetime(df["VALDATA"], format="%Y-%m-%dT%H:%M:%S")
    df = df.rename(columns={"VALDATA": "Date"})
    df = df.set_index("Date")

    df["VALVALOR"] = pd.to_numeric(df["VALVALOR"], errors="coerce")
    df = df.rename(columns={"VALVALOR": code})

    return df


IpeaUrlParams = TypedDict(
    "IpeaUrlParams",
    {
        "$select": str,
        "$filter": str,
    },
    total=False,
)


def build_url(
    code: str,
    start: Optional[str],
    end: Optional[str],
    last_n: Optional[int],
    metadata: IpeaMetadata,
) -> Tuple[str, IpeaUrlParams]:
    params: IpeaUrlParams
    params = {"$select": "VALDATA,VALVALOR"}

    url = (
        f"http://ipeadata2-homologa.ipea.gov.br/api/v1/ValoresSerie(SERCODIGO='{code}')"
    )

    max_date = (
        datetime.fromisoformat(metadata["SERMAXDATA"])
        if metadata["SERMAXDATA"]
        else datetime.utcnow()
    )

    min_date = (
        datetime.fromisoformat(metadata["SERMINDATA"])
        if metadata["SERMINDATA"]
        else datetime.utcnow()
    )

    if last_n:
        periodicity = metadata["PERNOME"]
        if periodicity == "Anual":
            offset_date = max_date - relativedelta(years=last_n)
        elif periodicity == "Quadrienal":
            offset_date = max_date - relativedelta(years=4 * last_n)
        elif periodicity == "Quinquenal":
            offset_date = max_date - relativedelta(years=5 * last_n)
        elif periodicity == "Decenal":
            offset_date = max_date - relativedelta(years=10 * last_n)
        elif periodicity == "Trimestral":
            offset_date = max_date - relativedelta(months=3 * last_n)
        elif periodicity == "Mensal":
            offset_date = max_date - relativedelta(months=last_n)
        elif periodicity == "Irregular":
            offset_date = max_date
        else:
            offset_date = max_date

        params["$filter"] = f"VALDATA gt {offset_date.isoformat()}"
    else:
        if start:
            start = (
                dates.parse_start_date(start)
                .replace(tzinfo=min_date.tzinfo)
                .isoformat()
            )

        if end:
            end = dates.parse_end_date(end).replace(tzinfo=max_date.tzinfo).isoformat()

        date_filter = ipea_filter_by_date(start, end)
        if date_filter:
            params["$filter"] = date_filter

    return url, params


def ipea_filter_by_date(start: str = None, end: str = None) -> str:
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
