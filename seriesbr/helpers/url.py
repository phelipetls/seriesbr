import re
from datetime import datetime
from .utils import cat, isiterable
from .ipea_metadata_list import ipea_metadata_list

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
            if re.search("(CODIGO|NUMERICA)$", metadata):
                metadata_filters.append(f"{metadata} eq {value}")
            else:
                metadata_filters.append(f"contains({metadata},'{value}')")
            filter_by_metadata = " and " if filter_by_name else ""
            filter_by_metadata += " and ".join(metadata_filters)
    return f"{prefix}{filter_by_name}{filter_by_metadata}"


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
    elif isinstance(classifications, int) or isinstance(classifications, str):
        return f"classificacao={classifications}[all]"
    elif isinstance(classifications, list):
        piped_classifications = '|'.join([f"{classification}[all]" for classification in classifications])
        return f"classificacao={piped_classifications}"
    else:
        return ""


def ibge_build_dates_query(start=None, end=None, last_n=None, month=True):
    """
    Auxiliary function to build the date part
    of the URL.
    """
    if month:
        today = datetime.today().strftime("%Y%m")
    else:
        today = datetime.today().strftime("%Y")
        start = start[:-2]
        end = end[:-2]
    if last_n:
        dates = f"/periodos/-{last_n}"
    elif start and end:
        dates = f"/periodos/{start}-{end}"
    elif start:
        dates = f"/periodos/{start}-{today}"
    elif end:
        dates = f"/periodos/{'190001' if month else '1900'}-{end}"
    return dates


def ibge_build_variables_query(variables):
    if isiterable(variables):
        return f"/variaveis/{cat(variables, '|')}"
    elif variables:
        return f"/variaveis/{variables}"
    else:
        return f"/variaveis"


def ibge_build_location_query(city, state, macroregion, microregion, mesoregion, brazil):
    # note-to-self: http://api.sidra.ibge.gov.br/desctabapi.aspx?c=136
    base = "&localidades="
    query = []
    if city:
        query.append(f"N6[{cat(city, '|') if city != 'all' else city}]")
    if state:
        query.append(f"N3[{cat(state, ',') if state != 'all' else state}]")
    if macroregion:
        query.append(f"N2[{cat(macroregion, ',') if macroregion != 'all' else macroregion}]")
    if mesoregion:
        query.append(f"N7[{cat(mesoregion, ',') if mesoregion != 'all' else mesoregion}]")
    if microregion:
        query.append(f"N9[{cat(microregion, ',') if microregion != 'all' else microregion}]")
    if brazil:
        query.append("BR")
    if all([location is None for location in [city, state, macroregion, microregion, mesoregion]]):
        return f"{base}BR"
    return base + "|".join(query)
