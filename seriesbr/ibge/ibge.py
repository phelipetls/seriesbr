import pandas as pd
from seriesbr.utils import requests
from . import url_builders, json_to_df

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
    url = url_builders.series.build_url(**locals())
    json = requests.get_json(url)
    metadata = get_metadata(table)
    frequency = metadata["periodicidade"]["frequencia"]
    df = json_to_df.series.build_df(json, frequency)
    return df


def get_metadata(table):
    """
    Get an IBGE table metadata.

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
    url = url_builders.metadata.build_url(table)
    json = requests.get_json(url)
    return json
