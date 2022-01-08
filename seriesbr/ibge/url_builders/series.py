from seriesbr.utils import misc, dates


def build_url(
    table,
    variables=None,
    start=None,
    end=None,
    last_n=None,
    municipalities=None,
    states=None,
    macroregions=None,
    microregions=None,
    mesoregions=None,
    brazil=None,
    classifications=None,
    frequency=None,
):
    url = f"https://servicodados.ibge.gov.br/api/v3/agregados/{table}"

    url += ibge_filter_by_date(start, end, last_n, frequency)
    url += ibge_filter_by_variable(variables)
    url += "?"
    url += ibge_filter_by_location(
        municipalities=municipalities,
        states=states,
        macroregions=macroregions,
        microregions=microregions,
        mesoregions=mesoregions,
        brazil=brazil,
    )
    url += ibge_filter_by_classification(classifications)
    url += "&view=flat"

    return url


def ibge_filter_by_classification(classifications=None):
    """
    Filter a table by classification and categories

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
    >>> url.ibge_filter_by_classification({1: [2, 3]})
    'classificacao=1[2,3]'

    >>> url.ibge_filter_by_classification([1, 2])
    'classificacao=1[all]|2[all]'

    >>> url.ibge_filter_by_classification(3)
    'classificacao=3[all]'
    """
    prefix = "&classificacao="

    if isinstance(classifications, dict):
        s = []
        for classification, categories in classifications.items():
            if not categories or categories == "all":
                s.append(f"{classification}[all]")
            else:
                joined_categories = misc.cat(categories, ",")
                s.append(f"{classification}[{joined_categories}]")
        return prefix + "|".join(s)

    elif isinstance(classifications, (int, str)):
        return prefix + f"{classifications}[all]"

    elif isinstance(classifications, list):
        joined_classifications = "|".join(
            [f"{classification}[all]" for classification in classifications]
        )
        return prefix + f"{joined_classifications}"

    return ""


def ibge_filter_by_date(start=None, end=None, last_n=None, freq=None):
    """
    Filter a table by date.

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
    >>> url.ibge_filter_by_date(last_n=5)
    '/periodos/-5'
    >>> url.ibge_filter_by_date(start="012017")
    '/periodos/201701-201912'
    >>> url.ibge_filter_by_date(end="072017")
    '/periodos/190001-201707'
    >>> url.ibge_filter_by_date(start="052015", end="072017")
    '/periodos/201505-201707'
    """
    start, end = dates.parse_dates(start, end, "ibge")
    if last_n:
        return f"/periodos/-{last_n}"

    if freq == "trimestral":
        start = dates.month_to_quarter(start, "%Y%m").strftime("%Y%m")
        end = dates.month_to_quarter(end, "%Y%m").strftime("%Y%m")

    elif freq == "anual":
        start, end = start[:-2], end[:-2]

    return f"/periodos/{start}-{end}"


def ibge_filter_by_variable(variables=None):
    """
    Filter a table by variable.

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
    >>> url.ibge_filter_by_variable(100)
    '/variaveis/100'
    >>> url.ibge_filter_by_variable([1, 2, 3])
    '/variaveis/1|2|3'
    >>> url.ibge_filter_by_variable()
    '/variaveis'
    """
    if misc.is_iterable(variables):
        joined_variables = misc.cat(variables, "|")
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


def ibge_filter_by_location(**kwargs):
    """
    Filter a table by location.

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
    >>> url.ibge_filter_by_location()
    '&localidades=BR'
    >>> url.ibge_filter_by_location(cities=True)
    '&localidades=N6'
    >>> url.ibge_filter_by_location(cities=1)
    '&localidades=N6[1]'
    >>> url.ibge_filter_by_location(cities=[2, 3, 4])
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
            joined_codes = misc.cat(code, ",")
            query.append(f"{location_name}[{joined_codes}]")
        elif type(code) == int:
            query.append(f"{location_name}[{code}]")
        elif code:
            query.append(f"{location_name}")

    return prefix + "|".join(query)
