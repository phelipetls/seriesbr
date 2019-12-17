import pandas as pd
from .helpers.request import get_json
from .helpers.response import ibge_json_to_df
from .helpers.utils import do_search
from .helpers.lists import list_regions
from .helpers.url import (
    ibge_make_dates_query,
    ibge_make_variables_query,
    ibge_make_location_query,
    ibge_make_classification_query,
    locations_dict
)


def get_series(
    code,
    variables=None,
    start=None,
    end=None,
    last_n=None,
    city=None,
    state=None,
    macroregion=None,
    microregion=None,
    mesoregion=None,
    brazil=None,
    classifications=None,
):
    """
    Function to get variables associated with a aggregated variable of IBGE's
    SIDRA database.

    Parameters
    ----------
    code : int
        The code of the aggregated variable.

    variables : int or list of ints, default None
        Which variables to select (if None, return all of them).

    start : int or str, default None
        Initial date, month or day first.

    end : int or str, default None
        Final date, month or day first.

    last_n : int or str, default None
        Return only last n observations.

    city : str or int a list of them, default None
        Codes of the cities to be selected.

    state : str or int or a list of them, default None
        Codes of the states to be selected.

    macroregion : str or int or a list of them, default None
        Codes of the macroregions to be selected.

    microregion : str or int or a list of them, default None
        Codes of the microregion to be selected.

    mesoregion : str or int or a list of them, default None
        Codes of the mesoregions to be selected.

    classifications : dict, int, str or list, default None
        { classification : [categories], ... }
        classification1
        "classification1"
        list = [classification1, classification2, ... ]

    Returns
    -------
    pandas.DataFrame
        A DataFrame with series values and metadata.

    Examples
    --------
        >>> ibge.get_series(1419, last_n=1)
                   Nível Territorial  ...   Valor
        Date                          ...
        2019-11-01            Brasil  ...    0.51
        2019-11-01            Brasil  ...    3.12
        2019-11-01            Brasil  ...    3.27
        2019-11-01            Brasil  ...  100.00
    """
    baseurl = f"https://servicodados.ibge.gov.br/api/v3/agregados/{code}"
    frequency = get_frequency(code)
    dates = ibge_make_dates_query(start, end, last_n, frequency)
    variables = ibge_make_variables_query(variables)
    locations = ibge_make_location_query(city, state, macroregion, microregion, mesoregion, brazil)
    classifications = ibge_make_classification_query(classifications)
    url = f"{baseurl}{dates}{variables}?{classifications}{locations}&view=flat"
    return ibge_json_to_df(get_json(url), frequency)

## Get metadata


def get_frequency(aggregate_code):
    return list_periods(aggregate_code).loc["frequency", :].values


def get_metadata(aggregate_code):
    url = f"https://servicodados.ibge.gov.br/api/v3/agregados/{aggregate_code}/metadados"
    json = get_json(url)
    return pd.DataFrame.from_dict(json, orient="index", columns=["values"])

## List Metadata Functions


def search(*search, **searches):
    """
    Function to list all aggregated variables of IBGE.

    Parameters
    ----------
    search : str
        Strings to search.

    where : str, default "nome"
        Where to search.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with metadata about the aggregates.

    Examples
    --------
        >>> ibge.search("Índice", "Preços", pesquisa_nome="Pesquisa")
                id                                               nome pesquisa_id                                      pesquisa_nome
        2472  1399  Número de empresas comerciais, Unidades locais...          PB                         Pesquisa Anual de Comércio
        2957   379  Índice de Gini - recebimento médio mensal das ...          OF                  Pesquisa de Orçamentos Familiares
        3101    50  Folha de pagamento nominal por classes de indú...          DG          Pesquisa Industrial Mensal - Dados Gerais
        3102    49  Folha de pagamento nominal por tipo de índice ...          DG          Pesquisa Industrial Mensal - Dados Gerais
        3103    52  Folha de pagamento nominal por trabalhador por...          DG          Pesquisa Industrial Mensal - Dados Gerais
        ...    ...                                                ...         ...                                                ...
        5490   431  Valor do rendimento e Número-índice do rendime...          PD        Pesquisa Nacional por Amostra de Domicílios
        5491   430  Valor do rendimento e Número-índice do rendime...          PD        Pesquisa Nacional por Amostra de Domicílios
        5673    32  Custo médio m² em variação percentual, por tip...          SI  Sistema Nacional de Pesquisa de Custos e Índic...
        5674    34  Preços medianos, por materiais e serviços (sér...          SI  Sistema Nacional de Pesquisa de Custos e Índic...
        5675  2062  Preços medianos, por materiais e serviços (sér...          SI  Sistema Nacional de Pesquisa de Custos e Índic...
    """
    json = get_json("https://servicodados.ibge.gov.br/api/v3/agregados")
    df = pd.io.json.json_normalize(
        json, record_path="agregados", meta=["id", "nome"], meta_prefix="pesquisa_"
    )
    if search or searches:
        return do_search(df, search, searches)
    return df


def list_variables(aggregate_code, *search, **searches):
    """
    Function to list all variables associated with an aggregate of IBGE.

    Parameters
    ----------
    search : str
        Strings to search.

    where : str, default "nome"
        Where to search.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with all available variables of an aggregate.

    Examples
    --------
        >>> ibge.list_variables(1419)
             id                               variavel unidade
        0    63                 IPCA - Variação mensal       %
        1    69       IPCA - Variação acumulada no ano       %
        2  2265  IPCA - Variação acumulada em 12 meses       %
        3    66                     IPCA - Peso mensal       %
    """
    baseurl = "https://servicodados.ibge.gov.br/api/v3"
    query = f"/agregados/{aggregate_code}/variaveis/all?localidades=BR"
    url = f"{baseurl}{query}"
    json = get_json(url)
    df = pd.io.json.json_normalize(json).iloc[:, :3]
    if search or searches:
        return do_search(df, search, searches)
    return df


def list_locations(aggregate_code):
    """
    Function to list locations of a given aggregate.

    Parameters
    ----------
    aggregate_code : int or str
        Aggregate's code.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with the available locations for an aggregate.

    Examples
    --------
        >>> ibge.list_locations(1419)
          codes  parameters
        0    N1      brazil
        1    N6        city
        2    N7  mesoregion
    """
    baseurl = "https://servicodados.ibge.gov.br/api/v3"
    query = f"/agregados/{aggregate_code}/metadados"
    url = f"{baseurl}{query}"
    codes = get_json(url)["nivelTerritorial"]["Administrativo"]
    df = pd.DataFrame({"codes": codes})
    df["parameters"] = [locations_dict.get(code) for code in df.codes]
    return df


def list_periods(aggregate_code):
    """
    Function to list periods of a given aggregate.

    Parameters
    ----------
    aggregate_code : int or str
        Aggregate's code.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with the frequency, initial and final dates of an aggregate.

    Examples
    --------
        >>> ibge.list_periods(1419)
                    value
        frequency  mensal
        start      201201
        end        201911
    """
    baseurl = "https://servicodados.ibge.gov.br/api/v3"
    query = f"/agregados/{aggregate_code}/metadados"
    url = f"{baseurl}{query}"
    json = get_json(url)["periodicidade"]
    df = pd.DataFrame.from_dict(json, orient="index", columns=["value"])
    df.index = ["frequency", "start", "end"]
    return df


def list_classifications(aggregate_code, *search, **searches):
    """
    Function to list all classification of a given aggregate.

    Parameters
    ----------
    aggregate_code : int or str
        Aggregated variable's code.

    *search
        Strings to search in categories' names.

    **searches
        Keyword arguments where param is a column and
        value a string or list of strings.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with the classifications and their categories.

    Examples
    --------
        >>> ibge.list_classifications(1419)
                 id                                     nome unidade  nivel classificacao_id                      classificacao_nome
        0      7169                             Índice geral    None     -1              315  Geral, grupo, subgrupo, item e subitem
        1      7170                  1.Alimentação e bebidas    None     -1              315  Geral, grupo, subgrupo, item e subitem
        2      7171              11.Alimentação no domicílio    None     -1              315  Geral, grupo, subgrupo, item e subitem
        3      7172  1101.Cereais, leguminosas e oleaginosas    None     -1              315  Geral, grupo, subgrupo, item e subitem
        4      7173                            1101002.Arroz    None     -1              315  Geral, grupo, subgrupo, item e subitem
        ..      ...                                      ...     ...    ...              ...                                     ...
        459    7792                 9101008.Telefone celular    None     -1              315  Geral, grupo, subgrupo, item e subitem
        460  107688                9101018.Acesso à internet    None     -1              315  Geral, grupo, subgrupo, item e subitem
        461    7794              9101019.Aparelho telefônico    None     -1              315  Geral, grupo, subgrupo, item e subitem
        462   12429   9101021.Telefone com internet - pacote    None     -1              315  Geral, grupo, subgrupo, item e subitem
        463   12430   9101022.TV por assinatura com internet    None     -1              315  Geral, grupo, subgrupo, item e subitem
    """
    baseurl = "https://servicodados.ibge.gov.br/api/v3/agregados"
    url = f"{baseurl}/{aggregate_code}/metadados"
    json = get_json(url)
    classifications = json["classificacoes"]
    df = pd.io.json.json_normalize(
        classifications,
        "categorias",
        meta=["id", "nome"],
        meta_prefix="classificacao_"
    )
    if search or searches:
        return do_search(df, search, searches)
    return df


def list_states(*search, **searches):
    """
    Function to list all states and their codes.

    Parameters
    ----------
    aggregate_code : int or str
        Aggregated variable's code.

    *search
        Strings to search in categories' names.

    **searches
        Keyword arguments where param is a column and
        value a string or list of strings.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with the states and their codes.

    Examples
    --------
    """
    return list_regions("estados", search, searches)


def list_macroregions(*search, **searches):
    """
    Function to list all macroregions and their codes.

    Parameters
    ----------
    *search
        Strings to search in categories' names.

    **searches
        Keyword arguments where param is a column and
        value a string or list of strings.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with the macroregions and their codes.

    Examples
    --------
    """
    return list_regions("regioes", search, searches)


def list_cities(*search, **searches):
    """
    Function to list all cities and their codes.

    Parameters
    ----------
    *search
        Strings to search in categories' names.

    **searches
        Keyword arguments where param is a column and
        value a string or list of strings.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with the cities and their codes.

    Examples
    --------
    """
    return list_regions("municipios", search, searches)


def list_microregions(*search, **searches):
    """
    Function to list all microregions.

    Parameters
    ----------
    *search
        Strings to search in categories' names.

    **searches
        Keyword arguments where param is a column and
        value a string or list of strings.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with metadata about the microregions.

    Examples
    --------
    """
    return list_regions("microrregioes", search, searches)


def list_mesoregions(*search, **searches):
    """
    Function to list all mesoregions and their codes.

    Parameters
    ----------
    *search
        Strings to search in categories' names.

    **searches
        Keyword arguments where param is a column and
        value a string or list of strings.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with metadata about the mesoregions.

    Examples
    --------
    """
    return list_regions("mesorregioes", search, searches)

# vi: nowrap
