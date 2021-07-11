import re
import pandas as pd

from distutils.version import StrictVersion

OLD_PANDAS = StrictVersion(pd.__version__) <= StrictVersion("0.25.3")


def json_normalize(*args, **kwargs):
    """
    Wrapper for dealing with pd.io.json.json_normalize
    deprecation warnings
    """
    return (
        pd.io.json.json_normalize(*args, **kwargs)
        if OLD_PANDAS
        else pd.json_normalize(*args, **kwargs)
    )


def parse_arguments(*args):
    """
    Parse arguments into a dictionary.
    Used to help label time series.

    Returns
    -------
    tuple
        First element with codes and second element
        with names.

    Examples
    >>> utils.collect_args({"A": 1, "B": 2}, 100)
    {"A": 1, "B": 2, 100: 100}
    """
    d = {}
    for arg in args:
        if isinstance(arg, dict):
            d.update(arg)
        else:
            d.update({arg: arg})
    return d


def quote_if_str(something):
    """
    Put quote around if a string.

    Parameters
    ----------
    something
        Any object.
    """
    if isinstance(something, str):
        return f"'{something}'"
    return f"{something}"


def cat(something, sep):
    """
    Join any iterable, except strings, by
    a custom delimiter.

    Parameters
    ----------
    something : list
        List to be joined.

    sep : str
        Delimiter.
    """
    return sep.join(map(str, something)) if is_iterable(something) else something


def is_iterable(something):
    """
    Test if it is an iterable other than
    a string.

    Returns
    -------
    bool
        True if an iterable other than str,
        False otherwise.
    """
    try:
        iter(something)
    except TypeError:
        return False
    return True and not isinstance(something, str)


def search_df(df, name, cols=[]):
    """
    Wrapper around query method of a DataFrame.

    Raises
    ------
    ValueError
        If the user tries to search in a
        non-existent column.
    """
    columns = df.columns.tolist()

    # check if additional searched columns exist
    for col in cols:
        if col not in columns:
            raise ValueError(f"{col} is not an existing column.")

    query = build_query(name, cols)

    return df.query(query, engine="python")


def build_query(name, cols=None):
    # build regex string to search variable name
    regex = build_regex(name)
    name_search = f"nome.str.contains('{regex}')"

    other_searches = ""
    if cols:
        queries = []

        for colname, value in cols.items():
            regex = build_regex(value)
            queries.append(f"{colname}.str.contains('{regex}')")

        other_searches = " and " + " and ".join(queries)

    return name_search + other_searches


def search_list(df, search, searches):
    """Just search if a search parameter was provided."""
    if search or searches:
        return search_df(df, search, searches).reset_index(drop=True)
    return df


def build_regex(strings):
    """Build a regex to use with DataFrame query method."""
    # (?iu) sets unicode and ignore case flags
    flags = r"(?iu)"

    if is_iterable(strings):
        joined_strings = "|".join(map(str, strings))
        return f"{flags}{joined_strings}"

    return f"{flags}{strings}"
