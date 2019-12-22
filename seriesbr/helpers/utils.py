import re
import pandas as pd


def return_codes_and_names(*args):
    """
    Auxiliary function to label columns of a
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
    for arg in args:
        if isinstance(arg, dict):
            return arg.values(), arg.keys()
    return args, args


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
    return sep.join(map(str, something)) if isiterable(something) else something


def isiterable(something):
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


def do_search(df, search, searches):
    """
    Auxiliary function to search for regex
    in a column of a DataFrame.

    It builds a string to be passed to
    the query method of a DataFrame.

    Parameters
    ----------

    df : pandas.DataFrame

    search : list of strings

    searches : dict

    Raises
    ------
    ValueError
        If the user tries to search in a
        non-existent column.
    """
    df_cols = df.columns.tolist()
    for col in searches:
        if col not in df_cols:
            raise ValueError(f"{col} is a non-existing column.")
    regex = build_regex(search)
    name_search = f"nome.str.contains('{regex}')"
    if searches:
        other_searches = []
        for field, search in searches.items():
            regex = build_regex(search)
            other_searches.append(f"{field}.str.contains('{regex}')")
        other_searches = " and " + " and ".join(other_searches)
        return df.query(name_search + other_searches, engine='python')
    return df.query(name_search, engine='python')


def build_regex(strings):
    """
    Build regex by joining strings by '|'
    only if it is an iterable other than a str.
    """
    # (?iu) sets unicode and ignore case flags
    flags = r'(?iu)'
    if isiterable(strings):
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
