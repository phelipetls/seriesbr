import re
from .utils import cat, isiterable
from .ipea_metadata_list import ipea_metadata_list
from .dates import today_date, month_to_quarter, check_if_quarters, parse_dates

## IPEA


def ipea_make_select_query(fields):
    # to get the string
    # SERCODIGO,PERNOME,UNINOME,SERNOME,ANOTHERFILTER,ANOTHERFILTER
    # where ANOTHER must be something not alreay selected by default
    defaults = ["SERCODIGO", "SERNOME", "PERNOME", "UNINOME"]
    selected = defaults + [field for field in fields if field not in defaults]
    return f"?$select={','.join(selected)}"


def ipea_make_filter_query(name, fields):
    # to get the string "&$filter=contains(SERNOME,'name')
    # and contains(ANOTHER,'value') and contains(ANOTHER,'value')"
    if any([field not in ipea_metadata_list for field in fields]):
        raise ValueError(f"Can't search for {' or '.join(fields)}. Call ipea.list_fields() if you need help.")
    prefix = "&$filter="
    filter_by_name = f"contains(SERNOME,'{name}')" if name else ""
    filter_by_metadata = ""
    metadata_filters = []
    if fields:
        for metadata, value in fields.items():
            if re.search("(CODIGO|NUMERICA|STATUS)$", metadata):
                if isinstance(value, list):
                    metadata_filters.append("(" + " or ".join([f"{metadata} eq {quote_if_str(item)}" for item in value]) + ")")
                else:
                    metadata_filters.append(f"{metadata} eq {quote_if_str(value)}")
            else:
                metadata_filters.append(f"contains({metadata},'{value}')")
            filter_by_metadata = " and " if filter_by_name else ""
            filter_by_metadata += " and ".join(metadata_filters)
    return f"{prefix}{filter_by_name}{filter_by_metadata}"


def quote_if_str(something):
    return f"'{something}'" if isinstance(something, str) else f"{something}"


## IBGE


def ibge_build_classification_query(classifications=None):
    """
    Auxiliary function to build classifications
    part of the URL.
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


def ibge_build_dates_query(start=None, end=None, last_n=None, freq=None):
    """
    Auxiliary function to build the date part
    of the URL.
    """
    start, end = parse_dates(start, end, "ibge")
    if last_n:
        dates = f"/periodos/-{last_n}"
    else:
        if freq == "trimestral":
            if end == today_date().strftime("%Y%m"):
                end = month_to_quarter(today_date()).strftime("%Y%m")
            assert check_if_quarters((start, end)), "Invalid quarter. Choose a number between 1 and 4"
        elif freq == "anual":
            start, end = start[:-2], end[:-2]
        dates = f"/periodos/{start}-{end}"
    return dates


def ibge_build_variables_query(variables):
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


def ibge_build_location_query(city=None, state=None, macroregion=None, microregion=None, mesoregion=None, brazil=None):
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
