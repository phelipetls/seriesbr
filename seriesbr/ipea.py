import pandas as pd

from seriesbr.helpers import api, utils, dates, timeseries, metadata, search_results


def get_series(*args, start=None, end=None, **kwargs):
    """
    Get multiple IPEA time series.

    Parameters
    ----------

    *args : int, dict
        Arbitrary number of time series codes.

    start : str, optional
        Initial date.

    end : str, optional
        Final date.

    **kwargs
        Passed to pandas.concat

    Returns
    -------
    pandas.DataFrame
    """
    parsed_args = utils.parse_arguments(*args)

    return pd.concat(
        (
            get_timeseries(code, label, start=start, end=end)
            for label, code in parsed_args.items()
        ),
        axis="columns",
        sort=True,
        **kwargs,
    )


def get_timeseries(code, label=None, start=None, end=None):
    """Return a single IPEA time series."""
    assert isinstance(code, str), "Not a valid code format."

    url = "http://ipeadata2-homologa.ipea.gov.br/api/v1/"
    url += f"ValoresSerie(SERCODIGO='{code}')"
    url += "?$select=VALDATA,VALVALOR"

    start, end = dates.parse_dates(start, end, api="ipea")
    url += api.ipea_filter_by_date(start, end)

    return timeseries.ipea_json_to_df(url, code, label)


def search(*SERNOME, **metadata):
    """
    Search IPEA database.

    Parameters
    ----------
    *SERNOME
        Strings to search for in a time series name.

    **metadata
        Strings to search for in metadata.

    Returns
    -------
    pandas.DataFrame

    Examples
    --------
    >>> ipea.search("Taxa", "Juros", "Selic", "recursos livres", PERNOME="mensal", UNINOME="%").head()
            SERCODIGO                                            SERNOME PERNOME   UNINOME
    0    BM12_CRDTJ12  Operações de crédito - recursos direcionados -...  Mensal  (% a.a.)
    1  BM12_CRDTJPF12  Operações de crédito - recursos direcionados -...  Mensal  (% a.a.)
    2  BM12_CRDTJPJ12  Operações de crédito - recursos direcionados -...  Mensal  (% a.a.)
    3    BM12_CRLIN12  Operações de crédito - recursos livres - inadi...  Mensal       (%)
    4  BM12_CRLINPF12  Operações de crédito - recursos livres - inadi...  Mensal       (%)
    """
    url = "http://ipeadata2-homologa.ipea.gov.br/api/v1/"
    url += "Metadados"
    url += api.ipea_select(metadata)
    url += api.ipea_filter(SERNOME, metadata)

    return search_results.ipea_get_search_results(url)


def get_metadata(code):
    """
    Get metadata of an IPEA time series.

    Parameters
    ----------
    code : int or str

    Returns
    -------
    pandas.DataFrame

    Examples
    --------
    >>> ipea.get_metadata("BM12_TJOVER12").head()
                                                               values
    SERCODIGO                                           BM12_TJOVER12
    SERNOME                              Taxa de juros - Over / Selic
    SERCOMENTARIO   Quadro: Taxas de juros efetivas.  Para 1974-19...
    SERATUALIZACAO                      2019-12-17T05:06:00.793-02:00
    BASNOME                                            Macroeconômico
    """
    url = build_metadata_url(code)
    return metadata.ipea_metadata_to_df(url)


def build_metadata_url(code):
    return f"http://ipeadata2-homologa.ipea.gov.br/api/v1/Metadados('{code}')"
