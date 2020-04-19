import pandas as pd

from seriesbr.helpers import api, utils, dates, timeseries, metadata, lists, search_results


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
    codes_and_labels = utils.collect(*args)

    return pd.concat(
        (
            get_timeseries(code, label, start=start, end=end)
            for label, code in codes_and_labels.items()
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
    url += api.ipea_date(start, end)

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


def list_themes():
    """
    Function to list all themes available
    in the database.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with all available themes
        in IPEA's database.

    Examples
    --------
    >>> ipea.list_themes().head()
        TEMCODIGO  TEMCODIGO_PAI                  TEMNOME
    0          28            NaN             Agropecuária
    1          23            NaN       Assistência social
    2          10            NaN    Balanço de pagamentos
    3           7            NaN                   Câmbio
    4           5            NaN        Comércio exterior
    """
    return lists.list_metadata("Temas")


def list_countries():
    """
    Function to list all countries available
    in the database.

    Returns
    -------
    pandas.DataFrame

    Examples
    --------
    >>> ipea.list_countries().head()
      PAICODIGO         PAINOME
    0       ZAF   África do Sul
    1       DEU        Alemanha
    2      LATI  América Latina
    3       AGO          Angola
    4       SAU  Arábia Saudita
    """
    return lists.list_metadata("Paises")


def list_metadata():
    """
    Function to list all valid metadatas and their description.

    Returns
    -------
    pandas.DataFrame

    Examples
    --------
    >>> ipea.list_metadata().head()
                       Description
    SERNOME                   Name
    SERCODIGO                 Code
    PERNOME              Frequency
    UNINOME    Unit of measurement
    BASNOME           Basis's name
    """
    return pd.DataFrame.from_dict(
        metadata.ipea_metadata_list, orient="index", columns=["Description"]
    )


# vi: nowrap
