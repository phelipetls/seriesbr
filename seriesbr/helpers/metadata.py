from pandas import DataFrame
from .request import get_json


def bcb_metadata_to_df(url):
    """Convert a BCB time series metadata into a DataFrame."""
    json = get_json(url)["result"]["results"][0]
    return DataFrame.from_dict(json, orient="index", columns=["values"])


ipea_metadata_list = {
    "SERNOME": "Name",
    "SERCODIGO": "Code",
    "PERNOME": "Frequency",
    "UNINOME": "Unit of measurement",
    "BASNOME": "Basis's name",
    "TEMCODIGO": "Theme's code",
    "PAICODIGO": "Country / Region's code",
    "SERCOMENTARIO": "Comments/Notes",
    "FNTNOME": "Source's name",
    "FNTSIGLA": "Source's initials",
    "FNTURL": "Source's url",
    "MULNOME": "Multiplicative factor",
    "SERATUALIZACAO": "When it was last updated",
    "SERSTATUS": "Active ('A'), Inactive ('I')",
    "SERNUMERICA": "Numeric (1), Alphanumeric (0)",
}


def ipea_metadata_to_df(url):
    """Convert a IPEA time series metadata into a DataFrame."""
    json = get_json(url)["value"][0]
    return DataFrame.from_dict(json, orient="index", columns=["values"])


def ibge_metadata_to_df(url):
    """Convert a IBGE time series metadata into a DataFrame."""
    json = get_json(url)
    return DataFrame.from_dict(json, orient="index", columns=["values"])
