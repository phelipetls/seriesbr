from pandas import concat, DataFrame, to_datetime
from .helpers.dates import parse_dates
from .helpers.utils import return_codes_and_names
from .helpers.lists import list_metadata_helper
from .helpers.response import ipea_json_to_df
from .helpers.metadata import ipea_metadata_to_df
from .helpers.searching import ipea_get_search_results
from .helpers.ipea_metadata_list import ipea_metadata_list
from .helpers.url import (
    ipea_make_select_query,
    ipea_make_filter_query,
    ipea_make_dates_query,
)


def get_serie(code, name=None, start=None, end=None):
    """
    Auxiliary function to return a single time series
    from IPEA database.
    """
    assert isinstance(code, str), "Not a valid code format."
    baseurl = "http://ipeadata2-homologa.ipea.gov.br/api/v1/"
    resource_path = f"ValoresSerie(SERCODIGO='{code}')"
    select = "?$select=VALDATA,VALVALOR"
    start, end = parse_dates(start, end, api="ipea")
    dates = ipea_make_dates_query(start, end)
    url = f"{baseurl}{resource_path}{select}{dates}"
    return ipea_json_to_df(url, code, name)


def get_series(*codes, start=None, end=None, **kwargs):
    """
    Get multiple series into a DataFrame.

    Parameters
    ----------
    codes : dict, str
        Dictionary like {"name1": code1, "name2": code2}
        or a bunch of code strings, e.g. code1, code2.

    start : str
        Initial date, month or day first.

    end : str
        End date, month or day first.

    **kwargs
        Passed to pandas.concat.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with series' values.

    Examples
    --------
    >>> ipea.get_series("BM12_TJOVER12", "CAGED12_SALDO12", start="2018", end="03-2018")
                BM12_TJOVER12  CAGED12_SALDO12
    Date
    2018-01-01           0.58          77822.0
    2018-02-01           0.47          61188.0
    2018-03-01           0.53          56151.0
    """
    codes, names = return_codes_and_names(*codes)
    df = concat(
        (get_serie(code, name, start, end) for code, name in zip(codes, names)),
        axis="columns",
        sort=True,
        **kwargs,
    )
    df.index = to_datetime(df.index, format="%Y-%m-%dT%H:%M:%S")
    return df


def search(*SERNOME, **metadatas):
    """
    Function to search in IPEA's database.

    Parameters
    ----------
    *SERNOME
        String(s) to look up for in a series' name.

    **metadatas
        Keyword arguments where parameter is a valid metadata
        and value a str or list of str.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with the search results.

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
    baseurl = "http://ipeadata2-homologa.ipea.gov.br/api/v1/"
    resource_path = "Metadados"
    select_query = ipea_make_select_query(metadatas)
    filter_query = ipea_make_filter_query(SERNOME, metadatas)
    url = f"{baseurl}{resource_path}{select_query}{filter_query}"
    return ipea_get_search_results(url)


def get_metadata(code):
    """
    Get metadata of a series specified
    by the a code.

    Parameters
    ----------
    code : int or str

    Returns
    -------
    pandas.DataFrame
        A DataFrame with series' metadata.

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
    baseurl = "http://ipeadata2-homologa.ipea.gov.br/api/v1/"
    resource_path = f"Metadados('{code}')"
    url = f"{baseurl}{resource_path}"
    return ipea_metadata_to_df(url)


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
    return list_metadata_helper("Temas")


def list_countries():
    """
    Function to list all countries available
    in the database.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with all available countries
        in IPEA's database.

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
    return list_metadata_helper("Paises")


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
    return DataFrame.from_dict(
        ipea_metadata_list, orient="index", columns=["Description"]
    )


# vi: nowrap
