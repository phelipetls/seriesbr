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
        url, params = url_builders.series.build_url(code, start, end, last_n)
        json = requests.get_json(url, params=params)
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
    url, params = url_builders.metadata.build_url(code)
    json = requests.get_json(url, params=params)
    return json["result"]["results"][0]
