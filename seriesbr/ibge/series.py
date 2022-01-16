import requests
import pandas as pd

from seriesbr.utils import session, dates, misc
from .metadata import get_metadata
from datetime import datetime
from typing import List, Union, Literal, Optional

BASEURL = "https://servicodados.ibge.gov.br/api/v3/agregados/"

IbgeFrequency = Union[Literal["mensal"], Literal["trimestral"], Literal["anual"]]
VariableValue = Union[int, str, List[int], List[str]]
LocationValue = Union[bool, int, List[int]]
ClassificationValue = Union[int, List[int], dict]


def get_series(
    table: int,
    variables: VariableValue = None,
    start: str = None,
    end: str = None,
    last_n: int = None,
    municipalities: LocationValue = None,
    states: LocationValue = None,
    macroregions: LocationValue = None,
    microregions: LocationValue = None,
    mesoregions: LocationValue = None,
    brazil: bool = None,
    classifications: ClassificationValue = None,
) -> pd.DataFrame:
    """
    Get an IBGE table

    Parameters
    ----------
    table : int
        Table code.

    variables : int or list of ints, optional
        Variables codes.

    start : int or str, optional
        Initial date, month or day first.

    end : int or str, optional
        Final date, month or day first.

    last_n : int or str, optional
        Return only last n observations.

    municipalities : str, int, bool a list, optional

    states : str, int, bool or a list, optional

    macroregions : str, int, bool or a list, optional

    microregions : str, int, bool or a list, optional

    mesoregions : str, int, bool or a list, optional

    classifications : dict, int, str or list, optional

    Returns
    -------
    pandas.DataFrame
        A DataFrame with series values and metadata.

    Examples
    --------
    >>> ibge.get_series(1419, start="11-2019", end="11-2019")
                Nível Territorial                              Variável   Geral, grupo, subgrupo, item e subitem   Valor
    Date
    2019-11-01            Brasil                 IPCA - Variação mensal   Índice geral                              0.51
    2019-11-01            Brasil       IPCA - Variação acumulada no ano   Índice geral                              3.12
    2019-11-01            Brasil  IPCA - Variação acumulada em 12 meses   Índice geral                              3.27
    2019-11-01            Brasil                     IPCA - Peso mensal   Índice geral                            100.00
    """
    metadata = get_metadata(table)
    frequency: IbgeFrequency = metadata["periodicidade"]["frequencia"]

    url = build_url(
        table,
        metadata,
        frequency,
        variables=variables,
        start=start,
        end=end,
        last_n=last_n,
        municipalities=municipalities,
        states=states,
        macroregions=macroregions,
        microregions=microregions,
        mesoregions=mesoregions,
        brazil=brazil,
        classifications=classifications,
    )

    try:
        response = session.get(url)
        json = response.json()
        df = build_df(json, frequency)
        return df
    except requests.exceptions.HTTPError as error:
        if error.response.status_code == 500:
            print(
                "A consulta pode ter retornado mais que 100.000 linhas. "
                "Tente adicionar mais filtros."
            )
        raise error


def get_date_format(freq: IbgeFrequency) -> str:
    formats = {"mensal": "%Y%m", "anual": "%Y", "trimestral": "%Y0%q"}
    return formats[freq]


def format_date(date: datetime, frequency: IbgeFrequency) -> str:
    if frequency == "trimestral":
        period = pd.Period(year=date.year, month=date.month, day=date.day, freq="M")
        return period.strftime("%Y0%q")

    # TODO: handle semester frequency

    return date.strftime(get_date_format(frequency))


ibge_columns = {
    "territory_code": "NC",
    "territory_name": "NN",
    "unit_of_measurement_code": "MC",
    "unit_of_measurement_name": "MN",
    "value": "V",
    "location_code": "D1C",
    "location_name": "D1N",
    "period_code": "D2C",
    "period_name": "D2N",
    "variable_name": "D3C",
    "variable_code": "D3N",
    "classification_code": "D4C",
    "classification_name": "D4N",
}

selected_ibge_columns = [
    ibge_columns["value"],
    ibge_columns["location_code"],
    ibge_columns["period_code"],
    ibge_columns["variable_name"],
    ibge_columns["variable_code"],
    ibge_columns["classification_name"],
]


def build_df(json: dict, freq: IbgeFrequency) -> pd.DataFrame:
    columns, data = json[0], json[1:]

    date_column = columns["D2C"]

    df = pd.DataFrame(data)
    df = df.loc[:, selected_ibge_columns]

    df.columns = [
        label for code, label in columns.items() if code in selected_ibge_columns
    ]

    if freq == "trimestral":

        def to_quarterly_period(date_str: str) -> pd.Period:
            """Converts a string like 'YYYYmm' into a quarterly period."""
            year_str, quarter_str = date_str[:4], date_str[4:]
            year, quarter = int(year_str), int(quarter_str)
            return pd.Period(year=year, quarter=quarter, freq="Q").to_timestamp()

        df[date_column] = df[date_column].apply(to_quarterly_period)
    else:
        df[date_column] = pd.to_datetime(df[date_column], format=get_date_format(freq))

    df = df.set_index(date_column)
    df = df.rename_axis("Date")

    df["Valor"] = pd.to_numeric(df["Valor"], errors="coerce")

    return df


def build_url(
    table: int,
    metadata: dict,
    frequency: IbgeFrequency,
    variables: VariableValue = None,
    start: str = None,
    end: str = None,
    last_n: int = None,
    municipalities: LocationValue = None,
    states: LocationValue = None,
    macroregions: LocationValue = None,
    microregions: LocationValue = None,
    mesoregions: LocationValue = None,
    brazil: bool = None,
    classifications: ClassificationValue = None,
) -> str:
    url = f"https://servicodados.ibge.gov.br/api/v3/agregados/{table}"

    url += ibge_filter_by_date(frequency, start, end, last_n)
    url += ibge_filter_by_variable(variables)
    url += "?"
    url += ibge_filter_by_location(
        metadata,
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


def ibge_filter_by_classification(classifications: ClassificationValue = None) -> str:
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


def ibge_filter_by_date(
    freq: IbgeFrequency,
    start: str = None,
    end: str = None,
    last_n: int = None,
) -> str:
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
    if last_n:
        return f"/periodos/-{last_n}"

    start_date = dates.parse_start_date(start) if start else dates.UNIX_EPOCH
    end_date = dates.parse_end_date(end) if end else datetime.today()

    return f"/periodos/{format_date(start_date, freq)}-{format_date(end_date, freq)}"


def ibge_filter_by_variable(variables=None) -> str:
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


def ibge_filter_by_location(metadata: dict, **kwargs: Optional[LocationValue]) -> str:
    """
    Filter a table by location.

    Parameters
    ----------
    metadata : dict
        Dictionary with IBGE table metadata.

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

    locations_dict = {k: v for k, v in kwargs.items() if v}

    if not locations_dict:
        return prefix + "BR"

    allowed_locations_codes = metadata["nivelTerritorial"]["Administrativo"]
    allowed_locations_names = [
        locations_codes_to_names[code] for code in allowed_locations_codes
    ]

    query = []

    for name, code in locations_dict.items():
        location_code = locations_names_to_codes.get(name)

        if location_code not in allowed_locations_codes:
            joined_allowed_locations_names = misc.cat(allowed_locations_names, ",")
            print(
                f"Você está tentando filtrar a tabela pela localidade '{name}', "
                f"mas somente as localidades '{joined_allowed_locations_names}' são permitidas."
            )
            raise ValueError

        if name == "brazil":
            query.append("BR")
        elif isinstance(code, list):
            joined_codes = misc.cat(code, ",")
            query.append(f"{location_code}[{joined_codes}]")
        elif type(code) == int:
            query.append(f"{location_code}[{code}]")
        else:
            query.append(f"{location_code}")

    return prefix + "|".join(query)
