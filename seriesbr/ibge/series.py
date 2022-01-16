import requests
import pandas as pd

from seriesbr.utils import session, dates
from .metadata import get_metadata
from datetime import datetime
from typing import List, Union, Literal, TypedDict, Optional, Tuple

BASEURL = "https://servicodados.ibge.gov.br/api/v3/agregados/"

IbgeFrequency = Union[Literal["mensal"], Literal["trimestral"], Literal["anual"]]

VariableInput = Union[int, str, List[int], List[str]]

Classification = int
Category = Union[int, List[int]]
ClassificationInput = Union[
    Classification, List[Classification], "dict[Classification, Category]"
]

LocationInput = Union[bool, int, List[int]]
LocationsInput = TypedDict(
    "LocationsInput",
    {
        "municipalities": Optional[LocationInput],
        "states": Optional[LocationInput],
        "macroregions": Optional[LocationInput],
        "mesoregions": Optional[LocationInput],
        "microregions": Optional[LocationInput],
        "brazil": Optional[Literal[True]],
    },
    total=False,
)


def get_series(
    table: int,
    variables: VariableInput = None,
    start: str = None,
    end: str = None,
    last_n: int = None,
    locations: LocationsInput = None,
    classifications: ClassificationInput = None,
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

    url, params = build_url(
        table,
        metadata,
        frequency,
        variables=variables,
        start=start,
        end=end,
        last_n=last_n,
        locations=locations,
        classifications=classifications,
    )

    try:
        response = session.get(url, params=params)
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
    ibge_columns["location_code"],
    ibge_columns["variable_name"],
    ibge_columns["variable_code"],
    ibge_columns["classification_name"],
]


def build_df(json: dict, freq: IbgeFrequency) -> pd.DataFrame:
    columns, data = json[0], json[1:]

    df = pd.DataFrame(data)

    df = df.rename(
        columns={ibge_columns["period_code"]: "Date", ibge_columns["value"]: "Valor"}
    )

    if freq == "trimestral":

        def to_quarterly_period(date_str: str) -> pd.Period:
            """Converts a string like 'YYYYmm' into a quarterly period."""
            year_str, quarter_str = date_str[:4], date_str[4:]
            year, quarter = int(year_str), int(quarter_str)
            return pd.Period(year=year, quarter=quarter, freq="Q").to_timestamp()

        df["Date"] = df["Date"].apply(to_quarterly_period)
    else:
        df["Date"] = pd.to_datetime(df["Date"], format=get_date_format(freq))
    df = df.set_index("Date")

    df = df.loc[:, ["Valor"] + selected_ibge_columns]
    df = df.rename(
        columns={
            code: label
            for code, label in columns.items()
            if code in selected_ibge_columns
        }
    )

    df["Valor"] = pd.to_numeric(df["Valor"], errors="coerce")

    return df


IbgeUrlParams = TypedDict(
    "IbgeUrlParams",
    {"classificacao": str, "localidades": str, "view": str},
    total=False,
)


def build_url(
    table: int,
    metadata: dict,
    frequency: IbgeFrequency,
    variables: VariableInput = None,
    start: str = None,
    end: str = None,
    last_n: int = None,
    locations: LocationsInput = None,
    classifications: ClassificationInput = None,
) -> Tuple[str, IbgeUrlParams]:
    url = f"https://servicodados.ibge.gov.br/api/v3/agregados/{table}"

    url += ibge_filter_by_date(frequency, start, end, last_n)
    url += ibge_filter_by_variable(variables)

    params: IbgeUrlParams = {"view": "flat"}
    params["localidades"] = ibge_get_location_params_value(locations, metadata)
    params["classificacao"] = ibge_get_classifications_params_value(classifications)

    return url, params


def ibge_get_classifications_params_value(classifications: ClassificationInput = None) -> str:
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
    '1[2,3]'

    >>> url.ibge_filter_by_classification([1, 2])
    '1[all]|2[all]'

    >>> url.ibge_filter_by_classification(3)
    '3[all]'
    """
    def format_classification_and_category(
        classification: Classification, category: Union[str, int]
    ):
        return f"{classification}[{category}]"

    if isinstance(classifications, dict):

        def parse_category(category: Category):
            if isinstance(category, list):
                joined_categories = ",".join(map(str, category))
                return joined_categories
            else:
                if category is True:
                    return "all"
                else:
                    return category

        result = [
            format_classification_and_category(classification, parse_category(category))
            for classification, category in classifications.items()
        ]

        return "|".join(result)

    elif isinstance(classifications, int):
        return format_classification_and_category(classifications, "all")

    elif isinstance(classifications, list):
        joined_classifications = "|".join(
            [
                format_classification_and_category(classification, "all")
                for classification in classifications
            ]
        )
        return f"{joined_classifications}"

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


def ibge_filter_by_variable(variables: VariableInput = None) -> str:
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
    if isinstance(variables, list):
        joined_variables = "|".join(map(str, variables))
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


def ibge_get_location_params_value(
    locations: Optional[LocationsInput], metadata: dict
) -> str:
    """
    Filter a table by location.

    Parameters
    ----------
    locations : dict
        Dictionary whose keys are one of the following:
            - municipalities
            - states
            - macroregions
            - mesoregions
            - microregions
            - brazil
        And values should the locations identifiers an int or a
        list of ints.

    metadata : dict
        Dictionary with IBGE table metadata.

    Returns
    -------
    str

    Examples
    --------
    >>> url.ibge_filter_by_location()
    'BR'
    >>> url.ibge_filter_by_location(cities=True)
    'N6'
    >>> url.ibge_filter_by_location(cities=1)
    'N6[1]'
    >>> url.ibge_filter_by_location(cities=[2, 3, 4])
    'N6[2,3,4]'
    """
    # NOTE: http://api.sidra.ibge.gov.br/desctabapi.aspx?c=136
    if not locations:
        return "BR"

    locations_dict = {name: value for name, value in locations.items() if value}

    allowed_locations_codes = metadata["nivelTerritorial"]["Administrativo"]
    allowed_locations_names = [
        locations_codes_to_names[code] for code in allowed_locations_codes
    ]

    value = []

    for name, code in locations_dict.items():
        location_code = locations_names_to_codes.get(name)

        if location_code not in allowed_locations_codes:
            joined_allowed_locations_names = ",".join(allowed_locations_names)
            print(
                f"Você está tentando filtrar a tabela pela localidade '{name}', "
                f"mas somente as localidades '{joined_allowed_locations_names}' são permitidas."
            )
            raise ValueError

        if name == "brazil":
            value.append("BR")
        elif isinstance(code, list):
            joined_codes = ",".join(map(str, code))
            value.append(f"{location_code}[{joined_codes}]")
        elif type(code) == int:
            value.append(f"{location_code}[{code}]")
        else:
            value.append(f"{location_code}")

    return "|".join(value)
