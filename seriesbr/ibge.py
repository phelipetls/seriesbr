import pandas as pd

from seriesbr.helpers import metadata, request, utils, timeseries, api

BASEURL = "https://servicodados.ibge.gov.br/api/v3/agregados/"


def get_series(
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
):
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
    frequency = get_frequency(table)
    url = build_series_url(**locals())

    return timeseries.ibge_json_to_df(url, frequency)


def get_frequency(table):
    """Get a table time frequency (periodicity)."""
    return list_periods(table).loc["frequencia", :].values


def build_url(table=""):
    """Return the url for a IBGE table."""
    return f"https://servicodados.ibge.gov.br/api/v3/agregados/{table}"


def build_series_url(
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
    frequency=None
):
    url = build_url(table)

    url += api.ibge_filter_by_date(start, end, last_n, frequency)
    url += api.ibge_filter_by_variable(variables)
    url += "?"
    url += api.ibge_filter_by_location(
        municipalities=municipalities,
        states=states,
        macroregions=macroregions,
        microregions=microregions,
        mesoregions=mesoregions,
        brazil=brazil,
    )
    url += api.ibge_filter_by_classification(classifications)
    url += "&view=flat"

    return url


def build_metadata_url(table):
    return build_url(table) + "/metadados"


def get_metadata(table):
    """
    Get a IBGE table metadata.

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
    url = build_metadata_url(table)
    return metadata.ibge_metadata_to_df(url)


def search(*search, **searches):
    """
    List all IBGE tables.

    Parameters
    ----------
    *search
        Strings to search for in a table name.

    **searches
        Strings to search in other field name,
        e.g. `pesquisa_nome`.

    Returns
    -------
    pandas.DataFrame

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
    url = build_url()
    json = request.get_json(url)

    df = utils.json_normalize(
        json, record_path="agregados", meta=["id", "nome"], meta_prefix="pesquisa_"
    )

    return utils.search_list(df, search, searches)


def list_periods(table):
    """
    List a time series periodicity.

    Examples
    --------
    >>> ibge.list_periods(1419)
               valores
    frequencia  mensal
    inicio      201201
    fim         201911
    """
    metadata = get_metadata(table)
    periods = metadata.loc["periodicidade"][0]

    return pd.DataFrame(periods.values(), index=periods.keys(), columns=["valores"])
