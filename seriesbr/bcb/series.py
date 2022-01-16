import pandas as pd

from seriesbr.utils import session, misc, dates
from datetime import datetime
from typing import Union, Tuple, TypedDict, Literal

DATE_FORMAT = "%d/%m/%Y"


def get_series(
    *args: Union[int, dict],
    start: str = None,
    end: str = None,
    last_n: int = None,
    **kwargs,
) -> pd.DataFrame:
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

    def get_timeseries(
        code: int,
        label: str = None,
        start: str = None,
        end: str = None,
        last_n: int = None,
    ) -> pd.DataFrame:
        url, params = build_url(code, start, end, last_n)
        response = session.get(url, params=params)
        json = response.json()
        return build_df(json, code, label)

    args_dict = misc.merge_into_dict(*args)

    return pd.concat(
        (
            get_timeseries(code, label, start=start, end=end, last_n=last_n)
            for label, code in args_dict.items()
        ),
        axis="columns",
        sort=True,
        **kwargs,
    )


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


def build_df(json: dict, code: int, label: str = None) -> pd.DataFrame:
    df = pd.DataFrame(json)

    df["valor"] = df["valor"].astype("float64")
    df["data"] = pd.to_datetime(df["data"], format="%d/%m/%Y")

    df = df.rename(columns={"data": "Date", "valor": label or code})
    df = df.set_index("Date")

    return df
