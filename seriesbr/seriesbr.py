import re
from pandas import concat
from . import bcb, ipea
from .helpers.utils import return_codes_and_names


def get_series(*codes, start=None, end=None, **kwargs):
    """
    Get multiple series from both BCB or IPEA.

    Parameters
    ----------
    codes : dict, str, int
        Dictionary like {"name1": cod1, "name2": cod2}
        or a bunch of code numbers, e.g. cod1, cod2.

    start : str, optional
        Initial date, month or day first.

    end : str, optional
        End date, month or day first.

    last_n : int, optional
        Ignore other arguments and get last n observations.

    **kwargs
        Passed to pandas.concat.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with series' values.
    """
    codes, names = return_codes_and_names(*codes)
    series = []
    for code, name in zip(codes, names):
        if re.search(r"^\d+$", str(code)):
            series.append(bcb.get_serie(code, name, start, end))
        else:
            series.append(ipea.get_serie(code, name, start, end))
    return concat(series, axis="columns", **kwargs)
