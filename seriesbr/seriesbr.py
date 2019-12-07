import re
from pandas import concat
from . import bcb, ipea
from .helpers.utils import return_codes_and_names


def get_series(*codes, start=None, end=None, **kwargs):
    codes, names = return_codes_and_names(*codes)
    series = []
    for code, name in zip(codes, names):
        if re.search(r"^\d+$", str(code)):
            series.append(bcb.get_serie(code, name, start, end))
        else:
            series.append(ipea.get_serie(code, name, start, end))
    return concat(series, axis="columns", **kwargs)
