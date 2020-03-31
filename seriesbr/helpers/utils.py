import re
import pandas as pd


def collect_codes_and_names(*args):
    """
    Auxiliary function to help label columns of a
    DataFrame.

    If it finds a dictionary, it will use its keys
    as labels and values as series' codes.

    Otherwise, the codes themselves will serve
    as columns' labels.

    Returns
    -------
    tuple
        First element with codes and second element
        with names.
    """
    codes, names = [], []
    for arg in args:
        if isinstance(arg, dict):
            for key, val in arg.items():
                codes.append(val)
                names.append(key)
        else:
            codes.append(arg)
            names.append(arg)
    return codes, names


def cat(something, sep):
    """
    Auxiliary function to join an iterable
    delimited by sep, forcing the join by
    coercing the items to be strings.

    Parameters
    ----------
    something : list
        List to be joined.

    sep : str
        Delimiter.

    Returns
    -------
    str
        String with values in something joined
        by sep.
    """
    return sep.join(map(str, something)) if is_iterable(something) else something


def is_iterable(something):
    """
    Auxiliary function to test if something is
    an iterable (unless it's a str).

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


def search_df(df, name, other=[]):
    """
    Auxiliary function to search for regex
    in a column of a DataFrame. This is a
    wrapper around the DataFrame query method.

    It builds a string to be passed to
    the query method of a DataFrame.

    Parameters
    ----------

    df : pandas.DataFrame

    search : list of strings

    other : dict

    Raises
    ------
    ValueError
        If the user tries to search in a
        non-existent column.
    """
    df_cols = df.columns.tolist()

    # check if additional searched columns exists
    for col in other:
        if col not in df_cols:
            raise ValueError(f"{col} is not an existing column.")

    # build regex string to search variable name
    regex = build_regex(name)
    name_search = f"nome.str.contains('{regex}')"

    # build regexes to search additional fields, if any
    if other:
        other_searches = []
        for field, search in other.items():
            regex = build_regex(search)
            other_searches.append(f"{field}.str.contains('{regex}')")
        other_searches = " and " + " and ".join(other_searches)
        return df.query(name_search + other_searches, engine="python")

    return df.query(name_search, engine="python")


def build_regex(strings):
    """
    Build regex by joining strings with '|' but
    only if it is an iterable other than a str.
    """
    # (?iu) sets unicode and ignore case flags
    flags = r'(?iu)'
    if is_iterable(strings):
        return f"{flags}{'|'.join(map(str, strings))}"
    return f"{flags}{strings}"


def clean_json(json):
    """
    Helper function to turn JSON into a DataFrame
    and clean its columns names.
    """
    df = pd.io.json.json_normalize(json, sep='_')
    df = df.rename(lambda x: '_'.join(re.split(r'_', x)[-2:]), axis='columns')
    return df

# vi: nowrap
