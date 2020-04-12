from pandas import concat

from .helpers.dates import parse_dates
from .helpers.utils import collect_codes_and_names
from .helpers.response import bcb_json_to_df
from .helpers.searching import bcb_get_search_results
from .helpers.metadata import bcb_metadata_to_df
from .helpers.generators import concatenate_series


@concatenate_series
def get_serie(code, name=None, start=None, end=None, last_n=None):
    """
    Auxiliary function to return a single time series
    from BCB database.
    """
    assert isinstance(code, (str, int)), "Not a valid code format."
    baseurl = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{code}/dados"
    if last_n:
        url = f"{baseurl}/ultimos/{last_n}?formato=json"
    else:
        start, end = parse_dates(start, end, api="bcb")
        dates = f"&dataInicial={start}&dataFinal={end}"
        url = f"{baseurl}?format=json{dates}"
    return bcb_json_to_df(url, code, name)


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
    # separate search terms
    first, others = search[0], search[1:]
    params = f"q={first}&rows={rows}&start={start}&sort=score desc"
    other_params = ""
    if others:
        other_params = f"&fq={'+'.join([name for name in others])}"
    url = f"{baseurl}{params}{other_params}"
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
