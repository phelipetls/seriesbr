import re
from .utils import cat, isiterable
from .ipea_metadata_list import ipea_metadata_list
from .dates import today_date, month_to_quarter, check_if_quarter, parse_dates

## IPEA


def ipea_make_dates_query(start, end):
    """
    Auxiliary function to return the right
    string for filtering dates.
    """
    dates = ""
    if start and end:
        dates = f"&$filter=VALDATA ge {start} and VALDATA le {end}"
    elif start:
        dates = f"&$filter=VALDATA ge {start}"
    elif end:
        dates = f"&$filter=VALDATA le {end}"
    return dates


def ipea_make_select_query(metadatas):
    """
    Auxiliary function to make select
    query for IBGE's web API.

    It loops through the keys of a dictionary
    and makes the string by joining them.

    Parameters
    ----------
    metadatas : dict
        Metadatas used in the search.

    Returns
    -------
    str
        A string to select metadatas.

    Examples
    --------
        >>> url.ipea_make_select_query("")
        '?$select=SERCODIGO,SERNOME,PERNOME,UNINOME'

        >>> url.ipea_make_select_query(["FNTNOME"])
        '?$select=SERCODIGO,SERNOME,PERNOME,UNINOME,FNTNOME'

        If a metadata is already selected by default, nothing changes:

        >>> url.ipea_make_select_query(["PERNOME"])
        '?$select=SERCODIGO,SERNOME,PERNOME,UNINOME'
    """
    # to get the string
    # SERCODIGO,PERNOME,UNINOME,SERNOME,ANOTHERFILTER,ANOTHERFILTER
    # where ANOTHER must be something not alreay selected by default
    defaults = ["SERCODIGO", "SERNOME", "PERNOME", "UNINOME"]
    selected = defaults + [metadata for metadata in metadatas if metadata not in defaults]
    return f"?$select={','.join(selected)}"


def ipea_make_filter_query(names, metadatas):
    """
    Auxiliary function to make filter
    query for IBGE's web API.

    Parameters
    ----------
    names : list of str
        Strings to filter by name.

    metadatas : dict
        Dictionary whose keys are metadatas
        and values strings (or list of strings)
        to look up for.

    Returns
    -------
    str
        A string to filter metadatas by values.

    Raises
    ------
    ValueError
        If not a valid metadata.

    Examples
    --------
        >>> url.ipea_make_filter_query("SELIC", {})
        "&$filter=contains(SERNOME,'SELIC')"

        >>> url.ipea_make_filter_query("SELIC", {"PERNOME": ["mensal", "trimestral"], "FNTNOME": "IBGE"})
        "&$filter=contains(SERNOME,'SELIC') and (contains(PERNOME,'mensal') or contains(PERNOME,'trimestral')) and contains(FNTNOME,'IBGE')"

        >>> url.ipea_make_filter_query("SELIC", {"SERSTATUS": "A", "SERNUMERICA": 1})
        "&$filter=contains(SERNOME,'SELIC') and SERSTATUS eq 'A' and SERNUMERICA eq 1"
    """
    if any([field not in ipea_metadata_list for field in metadatas]):
        raise ValueError(f"Can't search for {' or '.join(metadatas)}. Call ipea.list_metadata() if you need a hint.")
    prefix = "&$filter="
    filter_by_name = contains_operator("SERNOME", names) if names else ""
    filter_by_metadata = ""
    metadata_filters = []
    if metadatas:
        for metadata, value in metadatas.items():
            if re.search("(CODIGO|NUMERICA|STATUS)$", metadata):
                metadata_filters.append(equal_operator(metadata, value))
            else:
                metadata_filters.append(contains_operator(metadata, value))
        filter_by_metadata = " and " if filter_by_name else ""
        filter_by_metadata += " and ".join(metadata_filters)
    return f"{prefix}{filter_by_name}{filter_by_metadata}"


def contains_operator(metadata, values):
    """
    Auxiliary function to make string with
    OData's contains logical operator.
    """
    if isinstance(values, (list, tuple)):
        return "(" + " or ".join([f"contains({metadata},'{item}')" for item in values]) + ")"
    else:
        return f"contains({metadata},'{values}')"


def equal_operator(metadata, values):
    """
    Auxiliary function to make string with
    OData's equal logical operator.
    """
    if isinstance(values, (list, tuple)):
        return "(" + " or ".join([f"{metadata} eq {quote_if_str(item)}" for item in values]) + ")"
    else:
        return f"{metadata} eq {quote_if_str(values)}"


def quote_if_str(something):
    """
    Auxiliary function to put quotes around value
    if it is a string. Needed to make filter queries
    for OData's equal logical operator.
    """
    return f"'{something}'" if isinstance(something, str) else f"{something}"

## IBGE


def ibge_make_classification_query(classifications=None):
    """
    Auxiliary function to make classifications
    part of the URL.

    Parameters
    ----------
    classifications : int, str, list or dict
        Dict like { classification : category1, category2 }
        Int, str or list of classifications only.

    Returns
    -------
    str
        A string to filter by classifications / categories.

    Examples
    --------
        >>> url.ibge_make_classification_query({1: [2, 3]})
        'classificacao=1[2,3]'

        >>> url.ibge_make_classification_query([1, 2])
        'classificacao=1[all]|2[all]'

        >>> url.ibge_make_classification_query(3)
        'classificacao=3[all]'
    """
    if isinstance(classifications, dict):
        s = []
        for classification, category in classifications.items():
            if not category or category == "all":
                s.append(f"{classification}[all]")
            else:
                s.append(f"{classification}[{cat(category, ',')}]")
        return "classificacao=" + "|".join(s)
    elif isinstance(classifications, (int, str)):
        return f"classificacao={classifications}[all]"
    elif isinstance(classifications, list):
        piped_classifications = '|'.join([f"{classification}[all]" for classification in classifications])
        return f"classificacao={piped_classifications}"
    else:
        return ""


def ibge_make_dates_query(start=None, end=None, last_n=None, freq=None):
    """
    Auxiliary function to filter a time series'
    periods.

    Parameters
    ----------
    start : str
        Initial date string.

    end : str
        Final date string.

    last_n : str or int
        Get last n observations

    freq : str
        Time series frequency.

    Returns
    -------
    str
        A string to filter dates in IBGE's API.
    """
    start, end = parse_dates(start, end, "ibge")
    if last_n:
        return f"/periodos/-{last_n}"
    if freq == "trimestral":
        if end == today_date().strftime("%Y%m"):
            end = month_to_quarter(today_date()).strftime("%Y%m")
        assert check_if_quarter(
            (start, end)
        ), "Invalid quarter. Choose a number between 1 and 4"
    elif freq == "anual":
        start, end = start[:-2], end[:-2]
    return f"/periodos/{start}-{end}"


def ibge_make_variables_query(variables):
    """
    Auxiliary function to filter an IBGE's
    aggregate by variables.

    Parameters
    ----------
    variables : int or list of int
        The variables' codes.

    Returns
    -------
    str
        A string to filter variables in IBGE's API.
    """
    if isiterable(variables):
        return f"/variaveis/{cat(variables, '|')}"
    elif variables:
        return f"/variaveis/{variables}"
    else:
        return f"/variaveis"


locations_dict = {
    "N6": "city",
    "N3": "state",
    "N2": "macroregion",
    "N7": "mesoregion",
    "N9": "microregion",
    "N1": "brazil",
}


location_ids = {location: code for code, location in locations_dict.items()}


def ibge_make_location_query(city=None, state=None, macroregion=None, microregion=None, mesoregion=None, brazil=None):
    """
    Auxiliary function to filter an IBGE's
    aggregate by variables.

    Parameters
    ----------
    city
    state
    macroregion
    microregion
    mesoregion
    brazil

    Returns
    -------
    str
        A string to filter locations in IBGE's API.
    """
    # note-to-self: http://api.sidra.ibge.gov.br/desctabapi.aspx?c=136
    locations = vars()
    prefix = "&localidades="
    query = []
    if all([code is None for code in locations.values()]):
        return prefix + "BR"
    for location, codes in locations.items():
        if location == "brazil" and codes:
            query.append("BR")
        elif isinstance(codes, list):
            query.append(f"{location_ids[location]}[{cat(codes, ',')}]")
        elif type(codes) == int:
            query.append(f"{location_ids[location]}[{codes}]")
        elif codes:
            query.append(f"{location_ids[location]}[all]")
    return prefix + "|".join(query)

# vi: nowrap
