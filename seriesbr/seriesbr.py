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

    Examples
    --------
    >>> seriesbr.get_series("BM12_CRLIN12", 20786)
                BM12_CRLIN12  20786
    Date
    2011-03-01          4.41  26.22
    2011-04-01          4.55  27.01
    2011-05-01          4.72  26.84
    2011-06-01          4.71  26.72
    2011-07-01          4.89  26.91
    ...                  ...    ...
    2019-06-01          3.83  31.43
    2019-07-01          3.96  31.63
    2019-08-01          3.88  31.57
    2019-09-01          3.89  30.84
    2019-10-01          3.88  30.35
    """
    codes, names = return_codes_and_names(*codes)
    series = []
    for code, name in zip(codes, names):
        if re.search(r"^\d+$", str(code)):
            series.append(bcb.get_serie(code, name, start, end))
        else:
            series.append(ipea.get_serie(code, name, start, end))
    return concat(series, axis="columns", **kwargs)
