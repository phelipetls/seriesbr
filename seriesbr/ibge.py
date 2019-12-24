import pandas as pd
from .helpers.request import get_json
from .helpers.response import ibge_json_to_df
from .helpers.metadata import ibge_metadata_to_df
from .helpers.utils import do_search
from .helpers.lists import list_regions_helper
from .helpers.url import (
    ibge_make_dates_query,
    ibge_make_variables_query,
    ibge_make_locations_query,
    ibge_make_classifications_query,
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
    Function to get variables associated with an
    aggregate from IBGE's database.

    Parameters
    ----------
    code : int
        Aggregate's code.

    variables : int or list of ints, optional
        Which variables to select (if None, return all of them).

    start : int or str, optional
        Initial date, month or day first.

    end : int or str, optional
        Final date, month or day first.

    last_n : int or str, optional
        Return only last n observations.

    city : str, int, bool a list, optional
        Cities' codes.

    state : str, int, bool or a list, optional
        States' codes.

    macroregion : str, int, bool or a list, optional
        Macroregions' codes.

    microregion : str, int, bool or a list, optional
        Microregions' codes.

    mesoregion : str, int, bool or a list, optional
        Mesoregions' codes.

    classifications : dict, int, str or list, optional
        Classifications' / categories' codes.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with series values and metadata.

    Examples
    --------
    >>> ibge.get_series(1419, start="11-2019", end="11-2019")
               Nível Territorial                               Variável Geral, grupo, subgrupo, item e subitem   Valor
    Date
    2019-11-01            Brasil                 IPCA - Variação mensal                           Índice geral    0.51
    2019-11-01            Brasil       IPCA - Variação acumulada no ano                           Índice geral    3.12
    2019-11-01            Brasil  IPCA - Variação acumulada em 12 meses                           Índice geral    3.27
    2019-11-01            Brasil                     IPCA - Peso mensal                           Índice geral  100.00
    """
    baseurl = f"https://servicodados.ibge.gov.br/api/v3/agregados/{code}"
    frequency = get_frequency(code)
    dates = ibge_make_dates_query(start, end, last_n, frequency)
    variables = ibge_make_variables_query(variables)
    locations = ibge_make_locations_query(city, state, macroregion, microregion, mesoregion, brazil)
    classifications = ibge_make_classifications_query(classifications)
    url = f"{baseurl}{dates}{variables}?{classifications}{locations}&view=flat"
    return ibge_json_to_df(url, frequency)

## Get metadata


def get_frequency(aggregate):
    """
    Auxiliary function to get frequency of
    a time series from IBGE's database.

    This is needed because in case of a yearly time
    series, there can't be months in the url.
    """
    return list_periods(aggregate).loc["frequency", :].values


def get_metadata(aggregate):
    """
    Get metadata of a time series from IBGE's database.

    Parameters
    ----------
    aggregate : str
        Aggregate's code.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with metadata values.

    Examples
    --------
    >>> ibge.get_metadata(1419)
                                                                 values
    id                                                             1419
    nome              IPCA - Variação mensal, acumulada no ano, acum...
    URL                            http://sidra.ibge.gov.br/tabela/1419
    pesquisa              Índice Nacional de Preços ao Consumidor Amplo
    assunto                                           Índices de preços
    periodicidade     {'frequencia': 'mensal', 'inicio': 201201, 'fi...
    nivelTerritorial  {'Administrativo': ['N1', 'N6', 'N7'], 'Especi...
    variaveis         [{'id': 63, 'nome': 'IPCA - Variação mensal', ...
    classificacoes    [{'id': 315, 'nome': 'Geral, grupo, subgrupo, ...
    """
    url = f"https://servicodados.ibge.gov.br/api/v3/agregados/{aggregate}/metadados"
    return ibge_metadata_to_df(url)

## List Metadata Functions


def search(*search, **searches):
    """
    Function to list all aggregates in IBGE's database.

    Parameters
    ----------
    *search
        Strings to search in aggregates' names.

    **searches
        Strings to search in other columns.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with an aggregate's metadata.

    Examples
    --------
    >>> ibge.search("Índice", "Preços", pesquisa_nome="Pesquisa").head()
            id                                               nome pesquisa_id                              pesquisa_nome
    2472  1399  Número de empresas comerciais, Unidades locais...          PB                 Pesquisa Anual de Comércio
    2957   379  Índice de Gini - recebimento médio mensal das ...          OF          Pesquisa de Orçamentos Familiares
    3101    50  Folha de pagamento nominal por classes de indú...          DG  Pesquisa Industrial Mensal - Dados Gerais
    3102    49  Folha de pagamento nominal por tipo de índice ...          DG  Pesquisa Industrial Mensal - Dados Gerais
    3103    52  Folha de pagamento nominal por trabalhador por...          DG  Pesquisa Industrial Mensal - Dados Gerais
    """
    json = get_json("https://servicodados.ibge.gov.br/api/v3/agregados")
    df = pd.io.json.json_normalize(
        json, record_path="agregados", meta=["id", "nome"], meta_prefix="pesquisa_"
    )
    if search or searches:
        return do_search(df, search, searches)
    return df


def list_variables(aggregate, *search, **searches):
    """
    Function to list all variables associated with an aggregate.

    Parameters
    ----------
    aggregate : int or str
        Aggregate's code.

    *search
        Names to search for.

    **searches
        Strings to search in other columns.

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
    query = f"/agregados/{aggregate}/variaveis/all?localidades=BR"
    url = f"{baseurl}{query}"
    json = get_json(url)
    df = pd.io.json.json_normalize(json).iloc[:, :3]
    if search or searches:
        return do_search(df, search, searches)
    return df


def list_locations(aggregate):
    """
    Function to list locations of a given aggregate.

    Parameters
    ----------
    aggregate : int or str
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
    query = f"/agregados/{aggregate}/metadados"
    url = f"{baseurl}{query}"
    codes = get_json(url)["nivelTerritorial"]["Administrativo"]
    df = pd.DataFrame({"codes": codes})
    df["parameters"] = [locations_dict.get(code) for code in df.codes]
    return df


def list_periods(aggregate):
    """
    Function to list periods of a given aggregate.

    Parameters
    ----------
    aggregate : int or str
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
    query = f"/agregados/{aggregate}/metadados"
    url = f"{baseurl}{query}"
    json = get_json(url)["periodicidade"]
    df = pd.DataFrame.from_dict(json, orient="index", columns=["value"])
    df.index = ["frequency", "start", "end"]
    return df


def list_classifications(aggregate, *search, **searches):
    """
    Function to list all classification of a given aggregate.

    Parameters
    ----------
    aggregate : int or str
        Aggregate's code.

    *search
        Strings to search in categories' names.

    **searches
        Strings to search in other columns.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with the classifications and their categories.

    Examples
    --------
    >>> ibge.list_classifications(1419).head()
         id                                     nome unidade  nivel classificacao_id                      classificacao_nome
    0  7169                             Índice geral    None     -1              315  Geral, grupo, subgrupo, item e subitem
    1  7170                  1.Alimentação e bebidas    None     -1              315  Geral, grupo, subgrupo, item e subitem
    2  7171              11.Alimentação no domicílio    None     -1              315  Geral, grupo, subgrupo, item e subitem
    3  7172  1101.Cereais, leguminosas e oleaginosas    None     -1              315  Geral, grupo, subgrupo, item e subitem
    4  7173                            1101002.Arroz    None     -1              315  Geral, grupo, subgrupo, item e subitem
    """
    baseurl = "https://servicodados.ibge.gov.br/api/v3/agregados"
    url = f"{baseurl}/{aggregate}/metadados"
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
    aggregate : int or str
        Aggregate's code.

    *search
        Strings to search in states' names.

    **searches
        Strings to search in other columns.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with the states and their codes.

    Examples
    --------
    >>> ibge.list_states().head()
       id sigla      nome  regiao_id regiao_sigla regiao_nome
    0  11    RO  Rondônia          1            N       Norte
    1  12    AC      Acre          1            N       Norte
    2  13    AM  Amazonas          1            N       Norte
    3  14    RR   Roraima          1            N       Norte
    4  15    PA      Pará          1            N       Norte
    """
    return list_regions_helper("estados", search, searches)


def list_macroregions(*search, **searches):
    """
    Function to list all macroregions and their codes.

    Parameters
    ----------
    *search
        Strings to search in macroregions' names.

    **searches
        Strings to search in other columns.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with the macroregions and their codes.

    Examples
    --------
    >>> ibge.list_macroregions()
       id sigla          nome
    0   1     N         Norte
    1   2    NE      Nordeste
    2   3    SE       Sudeste
    3   4     S           Sul
    4   5    CO  Centro-Oeste
    """
    return list_regions_helper("regioes", search, searches)


def list_cities(*search, **searches):
    """
    Function to list all cities and their codes.

    Parameters
    ----------
    *search
        Strings to search in cities' names.

    **searches
        Strings to search in other columns.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with the cities and their codes.

    Examples
    --------
    >>> ibge.list_cities(UF_nome="Rio de Janeiro").head()
               id                nome  microrregiao_id       microrregiao_nome  mesorregiao_id     mesorregiao_nome  UF_id UF_sigla         UF_nome  regiao_id regiao_sigla regiao_nome
    3175  3300100      Angra dos Reis            33013     Baía da Ilha Grande            3305       Sul Fluminense     33       RJ  Rio de Janeiro          3           SE     Sudeste
    3176  3300159             Aperibé            33002  Santo Antônio de Pádua            3301  Noroeste Fluminense     33       RJ  Rio de Janeiro          3           SE     Sudeste
    3177  3300209            Araruama            33010                   Lagos            3304             Baixadas     33       RJ  Rio de Janeiro          3           SE     Sudeste
    3178  3300225               Areal            33005               Três Rios            3303    Centro Fluminense     33       RJ  Rio de Janeiro          3           SE     Sudeste
    3179  3300233  Armação dos Búzios            33010                   Lagos            3304             Baixadas     33       RJ  Rio de Janeiro          3           SE     Sudeste
    """
    return list_regions_helper("municipios", search, searches)


def list_microregions(*search, **searches):
    """
    Function to list all microregions.

    Parameters
    ----------
    *search
        Strings to search in microregions' names.

    **searches
        Strings to search in other columns.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with metadata about the microregions.

    Examples
    --------
    >>> ibge.list_microregions("Rio", mesorregiao_nome="Rio")
            id                   nome  mesorregiao_id                 mesorregiao_nome  UF_id UF_sigla         UF_nome  regiao_id regiao_sigla regiao_nome
    348  33018         Rio de Janeiro            3306  Metropolitana do Rio de Janeiro     33       RJ  Rio de Janeiro          3           SE     Sudeste
    352  35004  São José do Rio Preto            3501            São José do Rio Preto     35       SP       São Paulo          3           SE     Sudeste
    """
    return list_regions_helper("microrregioes", search, searches)


def list_mesoregions(*search, **searches):
    """
    Function to list all mesoregions and their codes.

    Parameters
    ----------
    *search
        Strings to search in mesoregions' names.

    **searches
        Strings to search in other columns.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with metadata about the mesoregions.

    Examples
    --------
    >>> ibge.list_mesoregions().head()
         id               nome  UF_id UF_sigla   UF_nome  regiao_id regiao_sigla regiao_nome
    0  1101    Madeira-Guaporé     11       RO  Rondônia          1            N       Norte
    1  1102  Leste Rondoniense     11       RO  Rondônia          1            N       Norte
    2  1201      Vale do Juruá     12       AC      Acre          1            N       Norte
    3  1202       Vale do Acre     12       AC      Acre          1            N       Norte
    4  1301   Norte Amazonense     13       AM  Amazonas          1            N       Norte
    """
    return list_regions_helper("mesorregioes", search, searches)

# vi: nowrap
