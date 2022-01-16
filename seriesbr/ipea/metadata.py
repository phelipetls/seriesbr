from seriesbr.utils import session
from typing import Tuple, TypedDict


class IpeaMetadata(TypedDict):
    SERCODIGO: str
    SERNOME: str
    SERCOMENTARIO: str
    SERATUALIZACAO: str
    BASNOME: str
    SERMAXDATA: str
    SERMINDATA: str
    PERNOME: str


def get_metadata(code: str) -> IpeaMetadata:
    """
    Get IPEA time series metadata.

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
    url, params = build_url(code)
    response = session.get(url, params=params)
    json = response.json()
    return json["value"][0]


def build_url(code: str) -> Tuple[str, None]:
    return f"http://ipeadata2-homologa.ipea.gov.br/api/v1/Metadados('{code}')", None
