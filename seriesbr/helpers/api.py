import re

from ..helpers.utils import cat, is_iterable
from ..helpers.odata import equal, contains
from ..helpers.dates import month_to_quarter, parse_dates
from ..helpers.metadata import ipea_metadata_list


def ipea_date(start=None, end=None):
    """
    Help filter an IPEA time series by date.

    Parameters
    ----------
    start : str
        Start date string.

    End : str
        End date string.

    Returns
    -------
    str
        A string to filter by dates.

    Examples
    --------
    >>> url.ipea_make_dates_query("2019-01-01T00:00:00-00:00", "2019-02-01T00:00:00-00:00")
    '&$filter=VALDATA ge 2019-01-01T00:00:00-00:00 and VALDATA le 2019-02-01T00:00:00-00:00'
    """
    dates = ""

    if start and end:
        dates = f"&$filter=VALDATA ge {start} and VALDATA le {end}"
    elif start:
        dates = f"&$filter=VALDATA ge {start}"
    elif end:
        dates = f"&$filter=VALDATA le {end}"

    return dates


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
    '?$select=SERCODIGO,SERNOME,PERNOME,UNINOME'
    >>> url.ipea_select(["FNTNOME"])
    '?$select=SERCODIGO,SERNOME,PERNOME,UNINOME,FNTNOME'
    >>> url.ipea_select(["PERNOME"])
    '?$select=SERCODIGO,SERNOME,PERNOME,UNINOME'
    """
    defaults = ["SERCODIGO", "SERNOME", "PERNOME", "UNINOME"]

    additional = [m for m in metadata if m not in defaults]
    columns = defaults + additional

    joined_columns = ",".join(columns)
    return f"?$select={joined_columns}"


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

    prefix = "&$filter="

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

    return f"{prefix}{filter_name}{filter_metadata}"


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


def ibge_classifications(classifications=None):
    """
    Help filter IBGE tables by classifications
    and categories.

    Parameters
    ----------
    classifications : int, str, list or dict
        Dictionary of classifications (keys)
        and categories (values) or a set of
        classifcations as int, str, or list.

    Returns
    -------
    str
        A valid string to filter by classifications
        and categories.

    Examples
    --------
    >>> url.ibge_classification({1: [2, 3]})
    'classificacao=1[2,3]'

    >>> url.ibge_classification([1, 2])
    'classificacao=1[all]|2[all]'

    >>> url.ibge_classification(3)
    'classificacao=3[all]'
    """
    if isinstance(classifications, dict):
        s = []
        for classification, categories in classifications.items():
            if not categories or categories == "all":
                s.append(f"{classification}[all]")
            else:
                joined_categories = cat(categories, ",")
                s.append(f"{classification}[{joined_categories}]")
        return "classificacao=" + "|".join(s)

    elif isinstance(classifications, (int, str)):
        return f"classificacao={classifications}[all]"

    elif isinstance(classifications, list):
        joined_classifications = "|".join(
            [f"{classification}[all]" for classification in classifications]
        )
        return f"classificacao={joined_classifications}"

    return ""


def ibge_dates(start=None, end=None, last_n=None, freq=None):
    """
    Help filter an IBGE table by date.

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
        A valid string to filter dates in IBGE's API.

    Examples
    --------
    >>> url.ibge_dates(last_n=5)
    '/periodos/-5'
    >>> url.ibge_dates(start="012017")
    '/periodos/201701-201912'
    >>> url.ibge_dates(end="072017")
    '/periodos/190001-201707'
    >>> url.ibge_dates(start="052015", end="072017")
    '/periodos/201505-201707'
    """
    start, end = parse_dates(start, end, "ibge")
    if last_n:
        return f"/periodos/-{last_n}"

    if freq == "trimestral":
        start = month_to_quarter(start, "%Y%m").strftime("%Y%m")
        end = month_to_quarter(end, "%Y%m").strftime("%Y%m")

    elif freq == "anual":
        start, end = start[:-2], end[:-2]

    return f"/periodos/{start}-{end}"


def ibge_variables(variables=None):
    """
    Help select specific variables of an IBGE table.

    Parameters
    ----------
    variables : int or list of int
        The variables' codes.

    Returns
    -------
    str
        A string to filter variables in IBGE's API.

    Examples
    --------
    >>> url.ibge_variables(100)
    '/variaveis/100'
    >>> url.ibge_variables([1, 2, 3])
    '/variaveis/1|2|3'
    >>> url.ibge_variables()
    '/variaveis'
    """
    if is_iterable(variables):
        joined_variables = cat(variables, "|")
        return f"/variaveis/{joined_variables}"
    elif variables:
        return f"/variaveis/{variables}"
    else:
        return "/variaveis"


locations_codes_to_names = {
    "N6": "municipalities",
    "N3": "states",
    "N2": "macroregions",
    "N7": "mesoregions",
    "N9": "microregions",
    "N1": "brazil",
}


locations_names_to_codes = {
    name: code for code, name in locations_codes_to_names.items()
}


def ibge_locations(**kwargs):
    """
    Help filter IBGE table by location.

    Parameters
    ----------
    **kwargs
        Keys must be one of these:
            - municipalities
            - states
            - macroregions
            - mesoregions
            - microregions
            - brazil
        And values should be an int or a
        list of ints.

    Returns
    -------
    str

    Examples
    --------
    >>> url.ibge_location()
    '&localidades=BR'
    >>> url.ibge_location(cities=True)
    '&localidades=N6'
    >>> url.ibge_location(cities=1)
    '&localidades=N6[1]'
    >>> url.ibge_location(cities=[2, 3, 4])
    '&localidades=N6[2,3,4]'
    """
    # NOTE: http://api.sidra.ibge.gov.br/desctabapi.aspx?c=136
    prefix = "&localidades="

    if not kwargs or all([v is None for v in kwargs.values()]):
        return prefix + "BR"

    query = []
    for name, code in kwargs.items():
        location_name = locations_names_to_codes.get(name)

        if name == "brazil" and code:
            query.append("BR")
        elif isinstance(code, list):
            joined_codes = cat(code, ",")
            query.append(f"{location_name}[{joined_codes}]")
        elif type(code) == int:
            query.append(f"{location_name}[{code}]")
        elif code:
            query.append(f"{location_name}")

    return prefix + "|".join(query)


# vi: nowrap
