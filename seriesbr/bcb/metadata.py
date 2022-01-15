from seriesbr.utils import session
from typing import Tuple


def get_metadata(code: int) -> dict:
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
    url, params = build_url(code)
    response = session.get(url, params=params)
    json = response.json()
    return json["result"]["results"][0]


def build_url(code: int) -> Tuple[str, dict]:
    params = {"fq": f"codigo_sgs:{code}"}
    return "https://dadosabertos.bcb.gov.br/api/3/action/package_search", params
