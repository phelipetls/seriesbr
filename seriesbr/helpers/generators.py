from functools import wraps
from pandas import concat
from .utils import collect_codes_and_names


def concatenate_series(get_series_function):
    @wraps(get_series_function)
    def wrapper(*codes, start=None, end=None, last_n=None, **kwargs):
        codes, names = collect_codes_and_names(*codes)
        df = concat(
            (
                get_series_function(code, name, start, end, last_n)
                for code, name in zip(codes, names)
            ),
            axis="columns",
            sort=True,
            **kwargs,
        )
        return df.sort_index()

    return wrapper
