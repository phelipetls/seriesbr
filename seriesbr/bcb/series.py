import pandas as pd

from seriesbr.utils import session, dates
from datetime import datetime
from typing import Tuple, TypedDict, Literal

DATE_FORMAT = "%d/%m/%Y"


def get_series(
    code: int,
    start: str = None,
    end: str = None,
    last_n: int = None,
) -> pd.DataFrame:
    """
    Get multiple BCB time series.

    Parameters
    ----------

    code : int
        Series identifier.

    start : str, optional
        Initial date.

    end : str, optional
        Final date.

    last_n : int, optional
        Number of last observations.

    Returns
    -------
    pandas.DataFrame
    """
    url, params = build_url(code, start, end, last_n)
    response = session.get(url, params=params)
    json = response.json()
    return build_df(json, code)


BcbOptionalUrlParams = TypedDict(
    "BcbOptionalUrlParams", {"dataInicial": str, "dataFinal": str}, total=False
)

BcbDefaultUrlParams = TypedDict(
    "BcbDefaultUrlParams",
    {"format": Literal["json"]},
)


class BcbUrlParams(BcbDefaultUrlParams, BcbOptionalUrlParams):
    pass


def build_url(
    code: int, start: str = None, end: str = None, last_n: int = None
) -> Tuple[str, BcbUrlParams]:
    url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{code}/dados"

    params: BcbUrlParams = {"format": "json"}

    if last_n:
        url += f"/ultimos/{last_n}"
        return url, params

    if not start and not end:
        return url, params

    start_date = dates.parse_start_date(start) if start else dates.UNIX_EPOCH
    params["dataInicial"] = start_date.strftime(DATE_FORMAT)

    end_date = dates.parse_end_date(end) if end else datetime.today()
    params["dataFinal"] = end_date.strftime(DATE_FORMAT)

    return url, params


def build_df(json: dict, code: int) -> pd.DataFrame:
    df = pd.DataFrame(json)

    df["valor"] = df["valor"].astype("float64")
    df["data"] = pd.to_datetime(df["data"], format="%d/%m/%Y")

    df = df.rename(columns={"data": "Date", "valor": str(code)})
    df = df.set_index("Date")

    return df
