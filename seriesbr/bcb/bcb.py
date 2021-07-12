import pandas as pd
from seriesbr.utils import requests, misc
from . import url_builders, json_to_df


def get_series(*args, start=None, end=None, last_n=None, **kwargs):
    """
    Get multiple BCB time series.

    Parameters
    ----------

    *args : int, dict
        Arbitrary number of time series codes.

    start : str, optional
        Initial date.

    end : str, optional
        Final date.

    last_n : int, optional
        Number of last observations.

    **kwargs
        Passed to pandas.concat

    Returns
    -------
    pandas.DataFrame
    """
    parsed_args = misc.parse_arguments(*args)

    def get_timeseries(code, name=None, start=None, end=None, last_n=None):
        url = url_builders.series.build_url(code, start, end, last_n)
        json = requests.get_json(url)
        return json_to_df.series.build_df(json, code, name)

    return pd.concat(
        (
            get_timeseries(code, label, start=start, end=end, last_n=last_n)
            for label, code in parsed_args.items()
        ),
        axis="columns",
        sort=True,
        **kwargs,
    )


def search(*strings, rows=10, start=1):
    """
    Search for a name in the BCB database.

    Parameters
    ----------
    rows : int, default 10
        How many results to show.

    start : int, default 1
        From which row to start showing the results.

    *strings
        Arbitrary number of strings to search.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with the search results.

    Examples
    --------
    >>> bcb.search("Atividade", "econômica", rows=5, start=2)
      codigo_sgs                                              title periodicidade    unidade_medida
    0      27738  Saldo das operações de crédito por atividade e...        mensal  Milhões de reais
    1      27742  Saldo das operações de crédito por atividade e...        mensal  Milhões de reais
    2      22039  Saldo das operações de crédito por atividade e...        mensal  Milhões de reais
    3      22041  Saldo das operações de crédito por atividade e...        mensal  Milhões de reais
    4      22027  Saldo das operações de crédito por atividade e...        mensal  Milhões de reais
    """
    url = url_builders.search.build_url(*strings, rows=rows, start=start)
    json = requests.get_json(url)
    df = json_to_df.search.build_df(json)
    return df


def get_metadata(code):
    """
    Get a BCB time series metadata.

    Parameters
    ----------
    code : str
        Time series' code.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with metadata values.

    Examples
    --------
    >>> bcb.get_metadata(20786).head()
                                                                        values
    referencias              <P><A href="http://www.bcb.gov.br/estatisticas...
    license_title            Licença Aberta para Bases de Dados (ODbL) do O...
    maintainer                  Banco Central do Brasil/Departamento Econômico
    relationships_as_object                                                 []
    vcge                     Política Econômica [http://vocab.e.gov.br/2011...
    """
    url = url_builders.metadata.build_url(code)
    json = requests.get_json(url)
    df = json_to_df.metadata.build_df(json)
    return df
