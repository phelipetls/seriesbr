from pandas import concat, to_datetime
from .helpers.dates import parse_dates
from .helpers.utils import return_codes_and_names
from .helpers.response import bcb_json_to_df
from .helpers.searching import bcb_get_search_results
from .helpers.metadata import bcb_metadata_to_df


def get_serie(code, name=None, start=None, end=None, last_n=None):
    """
    Auxiliary function to return a single time series
    from BCB database.
    """
    assert isinstance(code, str) or isinstance(code, int), "Not a valid code format."
    baseurl = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{code}/dados"
    if last_n:
        url = f"{baseurl}/ultimos/{last_n}?formato=json"
    else:
        start, end = parse_dates(start, end, api="bcb")
        dates = f"&dataInicial={start}" if start else start
        dates += f"&dataFinal={end}" if end else end
        url = f"{baseurl}?format=json{dates}"
    return bcb_json_to_df(url, code, name)


def get_series(*codes, start=None, end=None, last_n=None, **kwargs):
    """
    Get multiple series into a DataFrame.

    Parameters
    ----------
    codes : dict, str, int
        Dictionary like {"name1": cod1, "name2": cod2}
        or a bunch of code numbers, e.g. cod1, cod2.

    start : str, optional
        Initial date, month or day first.

    end : str, optional
        End date, month or day first.

    last_n : int, optional
        Ignore other arguments and get last n observations.

    **kwargs
        Passed to pandas.concat.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with series' values.

    Examples
    --------
    >>> bcb.get_series({"Spread": 20786}, start="02-2018", end="072018")
                Spread
    Date
    2018-02-01   33.97
    2018-03-01   33.66
    2018-04-01   33.03
    2018-05-01   30.92
    2018-06-01   29.43
    2018-07-01   29.39
    """
    assert codes, "You must pass at least one code."
    codes, names = return_codes_and_names(*codes)
    df = concat(
        (get_serie(code, name, start, end, last_n) for code, name in zip(codes, names)),
        axis="columns",
        sort=True,
        **kwargs,
    )
    df.index = to_datetime(df.index, format="%d/%m/%Y")
    return df


def search(*search, rows=10, start=1):
    """
    Search for a name in the SGS database.

    Parameters
    ----------
    rows : int, default 10
        How many results to show.

    start : int, default 1
        From which row to start showing the results.

    *search
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
    baseurl = "https://dadosabertos.bcb.gov.br/api/3/action/package_search?"
    params = f"q={search[0]}&rows={rows}&start={start}&sort=score desc"
    filter_params = ""
    if len(search) > 1:
        filter_params = f"&fq={'+'.join([name for name in search[1:]])}"
    url = f"{baseurl}{params}{filter_params}"
    return bcb_get_search_results(url)


def get_metadata(code):
    """
    Get metadata of a BCB's time series.

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
    baseurl = "https://dadosabertos.bcb.gov.br/api/3/action/package_search?"
    params = f"fq=codigo_sgs:{code}"
    url = f"{baseurl}{params}"
    return bcb_metadata_to_df(url)


# vi: nowrap
