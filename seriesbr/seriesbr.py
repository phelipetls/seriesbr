import re
from . import bcb, ipea, helpers
from pandas import concat


def get_series(*codes, start=None, end=None, **kwargs):
    codes, names = helpers.types.check_and_return_codes_and_names(*codes)
    series = []
    for code, name in zip(codes, names):
        if re.search(r"^\d+$", str(code)):
            series.append(bcb.get_serie(code, start, end, name))
        else:
            series.append(ipea.get_serie(code, start, end, name))
    return concat(series, axis="columns", **kwargs)
