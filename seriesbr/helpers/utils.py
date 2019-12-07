import re
import pandas as pd


def return_codes_and_names(*args):
    """
    Auxiliary function to return codes and names
    of the series.

    If it finds a dictionary, it will use its keys
    as names and values as codes.

    Otherwise, it will just return the requested
    codes as names, so the column names will be
    the codes themselves.
    """
    for arg in args:
        if isinstance(arg, dict):
            return arg.values(), arg.keys()
    return args, args


def cat(something, sep):
    """
    Auxiliary function to join an iterable if it
    is one, delimited by sep, forcing the join by
    coercing the items to be strings.
    """
    return sep.join(map(str, something)) if isiterable(something) else something


def isiterable(something):
    """
    Auxiliary function to test if something is
    an iterable or not.
    """
    try:
        iter(something)
    except TypeError:
        return False
    return True


def do_search(df, search, where, prefix=""):
    """
    Helper function to search for regex
    in a given column
    """
    # (?iu) sets unicode and ignore case flags
    to_search = r'(?iu)' + '|'.join(search)
    return df.query(f"{where}.str.contains(@to_search)", engine='python')


def clean_json(json):
    """
    Helper function to transform JSON into
    a DataFrame and clean its columns names.
    """
    df = pd.io.json.json_normalize(json, sep='_')
    df = df.rename(lambda x: x.replace('.', '_'), axis='columns')
    df = df.rename(lambda x: '_'.join(re.split(r'_', x)[-2:]), axis='columns')
    return df
