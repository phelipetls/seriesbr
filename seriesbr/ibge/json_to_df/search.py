import pandas as pd
from seriesbr.utils import misc


def build_df(json, *search, **searches):
    df = pd.json_normalize(
        json, record_path="agregados", meta=["id", "nome"], meta_prefix="pesquisa_"
    )
    return search_list(df, *search, **searches)


def build_regex(strings):
    """Build a regex to use with DataFrame query method."""
    # (?iu) sets unicode and ignore case flags
    flags = r"(?iu)"

    if misc.is_iterable(strings):
        joined_strings = "|".join(map(str, strings))
        return f"{flags}{joined_strings}"

    return f"{flags}{strings}"


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


def search_list(df, search, searches):
    """Just search if a search parameter was provided."""
    if search or searches:
        return search_df(df, search, searches).reset_index(drop=True)
    return df
