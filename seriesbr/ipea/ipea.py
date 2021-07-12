import pandas as pd
from seriesbr.utils import requests, misc
from . import url_builders, json_to_df


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
    parsed_args = misc.parse_arguments(*args)

    def get_timeseries(code, label=None, start=None, end=None):
        url, params = url_builders.series.build_url(code, start, end)
        json = requests.get_json(url, params=params)
        df = json_to_df.series.build_df(json, code, label)
        return df

    return pd.concat(
        (
            get_timeseries(code, label, start=start, end=end)
            for label, code in parsed_args.items()
        ),
        axis="columns",
        sort=True,
        **kwargs,
    )


def search(*code, **metadata):
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
    url, params = url_builders.search.build_url(*code, **metadata)
    json = requests.get_json(url, params=params)
    df = json_to_df.search.build_df(json)
    return df


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
    url, params = url_builders.metadata.build_url(code)
    json = requests.get_json(url, params=params)
    df = json_to_df.metadata.build_df(json)
    return df
