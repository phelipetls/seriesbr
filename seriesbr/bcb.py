import pandas as pd

from seriesbr.helpers import utils, timeseries, metadata, dates, search_results


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
    codes_and_labels = utils.collect(*args)

    return pd.concat(
        (
            get_timeseries(code, label, start=start, end=end, last_n=last_n)
            for label, code in codes_and_labels.items()
        ),
        axis="columns",
        sort=True,
        **kwargs,
    )


def get_timeseries(code, name=None, start=None, end=None, last_n=None):
    """Return a single BCB time series in a DataFrame."""
    url = build_url(code, start, end, last_n)

    return timeseries.bcb_json_to_df(url, code, name)


def build_url(code, start=None, end=None, last_n=None):
    """Return the url for a BCB time series."""
    assert isinstance(code, (str, int)), "Not a valid code format."

    url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{code}/dados"

    if last_n:
        url += f"/ultimos/{last_n}"
        url += "?format=json"
        return url

    url += "?format=json"

    start, end = dates.parse_dates(start, end, api="bcb")
    url += f"&dataInicial={start}&dataFinal={end}"

    return url


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
    url = build_search_url(*strings, rows=rows, start=start)
    return search_results.bcb_get_search_results(url)


def build_search_url(*strings, rows=10, start=1):
    """Return a URL to search in the BCB database."""
    url = "https://dadosabertos.bcb.gov.br/api/3/action/package_search?"

    first, others = strings[0], strings[1:]
    params = f"q={first}&rows={rows}&start={start}&sort=score desc"

    other_params = ""
    if others:
        joined_params = "+".join([str(s) for s in others])
        other_params = f"&fq={joined_params}"

    return f"{url}{params}{other_params}"


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
    url = build_metadata_url(code)
    return metadata.bcb_metadata_to_df(url)


def build_metadata_url(code):
    """Return a URL to search for a BCB time series metadata."""
    baseurl = "https://dadosabertos.bcb.gov.br/api/3/action/package_search?"
    params = f"fq=codigo_sgs:{code}"
    return f"{baseurl}{params}"


# vi: nowrap
