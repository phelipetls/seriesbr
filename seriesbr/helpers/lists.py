from pandas import DataFrame
from .request import get_json
from .utils import clean_json, do_search


# IBGE


def list_regions_helper(region, search, searches):
    """
    Auxiliary function to list information
    about a given location in IBGE's database.

    Parameters
    ----------
    region : str
        Kind of region to list (macroregion, state etc.)

    search : list
        Strings to search in names column.

    searches : dict
        Strings to search in other columns.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with the regions, filtered if specified.
    """
    url = f"https://servicodados.ibge.gov.br/api/v1/localidades/{region}"
    json = get_json(url)
    df = clean_json(json)
    if search or searches:
        return do_search(df, search, searches)
    return df


# IPEA


def list_metadata_helper(resource_path):
    """
    Auxiliary function to request metadata
    information about a IPEA's time series.

    Parameters
    ----------
    resource_path : str
        Which kind of information to be
        requested, e.g. themes, countries.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with the specified resource.
    """
    baseurl = "http://www.ipeadata.gov.br/api/odata4/"
    url = f"{baseurl}{resource_path}"
    json = get_json(url)["value"]
    return DataFrame(json)
