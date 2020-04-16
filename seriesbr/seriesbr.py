from pandas import concat
from seriesbr import bcb, ipea
from seriesbr.helpers import utils


def get_series(*args, start=None, end=None, **kwargs):
    """
    Get multiple series from both BCB or IPEA.

    Parameters
    ----------
    args : dict, str, int
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
    >>> seriesbr.get_series("BM12_CRLIN12", 20786, start="2015", end="2015")
                BM12_CRLIN12  20786
    Date
    2015-01-01          4.41  26.91
    2015-02-01          4.42  27.95
    2015-03-01          4.38  27.72
    2015-04-01          4.57  28.93
    2015-05-01          4.68  29.61
    2015-06-01          4.59  30.31
    2015-07-01          4.77  31.24
    2015-08-01          4.91  31.65
    2015-09-01          4.92  31.49
    2015-10-01          5.02  32.64
    2015-11-01          5.22  33.31
    2015-12-01          5.28  31.64
    """
    codes_and_labels = utils.collect(*args)
    series = []

    for label, code in codes_and_labels.items():
        if str(code).isnumeric():
            df = bcb.get_timeseries(code, label, start, end)
        else:
            df = ipea.get_timeseries(code, label, start, end)
        series.append(df)

    return concat(series, axis="columns", **kwargs)
