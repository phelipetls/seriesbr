import re
from seriesbr import utils


def build_url(*code, **metadata):
    url = "http://ipeadata2-homologa.ipea.gov.br/api/v1/Metadados"
    params = {"$select": ipea_select(metadata), "$filter": ipea_filter(*code, metadata)}
    return url, params


def ipea_select(metadata=[]):
    """
    Help select additional IPEA time series
    metadata, if not already selected by default.

    Parameters
    ----------
    metadata : list

    Examples
    --------
    >>> url.ipea_select()
    'SERCODIGO,SERNOME,PERNOME,UNINOME'
    >>> url.ipea_select(["FNTNOME"])
    'SERCODIGO,SERNOME,PERNOME,UNINOME,FNTNOME'
    >>> url.ipea_select(["PERNOME"])
    'SERCODIGO,SERNOME,PERNOME,UNINOME'
    """
    defaults = ["SERCODIGO", "SERNOME", "PERNOME", "UNINOME"]

    additional = [m for m in metadata if m not in defaults]
    columns = defaults + additional

    return ",".join(columns)


def ipea_filter(names=None, metadata={}):
    """
    Help filter IPEA time series metadata.

    Parameters
    ----------
    names : list of str
        Strings to search for in time series name.

    metadata : dict
        Dictionary to search strings in specific
        metadata, e.g. { "metadata": ["str"] }.

    Raises
    ------
    ValueError

    Examples
    --------
    >>> url.ipea_filter("SELIC")
    "&$filter=contains(SERNOME,'SELIC')"
    >>> url.ipea_filter("SELIC", {"PERNOME": ["mensal", "trimestral"], "FNTNOME": "IBGE"})
    "&$filter=contains(SERNOME,'SELIC') and (contains(PERNOME,'mensal') or contains(PERNOME,'trimestral')) and contains(FNTNOME,'IBGE')"
    >>> url.ipea_filter("SELIC", {"SERSTATUS": "A", "SERNUMERICA": 1})
    "&$filter=contains(SERNOME,'SELIC') and SERSTATUS eq 'A' and SERNUMERICA eq 1"
    """
    raise_if_invalid_metadata(metadata)

    # filter by name
    filter_name = contains("SERNOME", names, " and ") if names else ""

    # start building string to filter by additional metadata
    filter_metadata = ""
    if metadata:
        metadata_filters = []

        for metadata, value in metadata.items():
            if re.search("(CODIGO|NUMERICA|STATUS)$", metadata):
                s = equal(metadata, value)
                metadata_filters.append(s)
            else:
                s = contains(metadata, value)
                metadata_filters.append(s)

        filter_metadata = " and " if filter_name else ""
        filter_metadata += " and ".join(metadata_filters)

    return f"{filter_name}{filter_metadata}"


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


def raise_if_invalid_metadata(metadata):
    """Friendly error message in case of an invalid metadata."""
    invalid_metadata = []
    for m in metadata:
        if m not in ipea_metadata_list:
            invalid_metadata.append(m)

    if invalid_metadata:
        joined_invalid_metadata = ", ".join(invalid_metadata)
        error_msg = f"{joined_invalid_metadata}: non-valid metadata."
        error_msg += "\nCall ipea.list_metadata() if you need help."
        raise ValueError(error_msg)


def contains(metadata, values, logical_operator=" or "):
    """
    Build contains operator for OData API query.

    Examples
    --------
    >>> url.contains("FNTNOME", ["A", "B"])
    "(contains('FNTNOME','A') or contains('FNTNOME','B'))"
    """

    if isinstance(values, (list, tuple)):
        filters = [f"contains({metadata},'{item}')" for item in values]
        joined_filters = logical_operator.join(filters)
        return f"({joined_filters})"

    return f"contains({metadata},'{values}')"


def equal(metadata, values, logical_operator=" or "):
    """
    Build equal operator for OData API query.

    Examples
    --------
    >>> url.equal("SERNUMERICA", [1, "A"])
    "('SERNUMERICA' eq 1 or 'SERNUMERICA', eq 'A')"
    """

    if isinstance(values, (list, tuple)):
        filters = [f"{metadata} eq {utils.misc.quote_if_str(item)}" for item in values]
        joined_filters = logical_operator.join(filters)
        return f"({joined_filters})"

    return f"{metadata} eq {utils.misc.quote_if_str(values)}"
