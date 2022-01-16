from seriesbr.utils import session
from typing import Tuple


def get_metadata(table: int) -> dict:
    """
    Get an IBGE table metadata.

    Examples
    --------
    >>> ibge.get_metadata(1419)
                                                                 values
    id                                                             1419
    nome              IPCA - Variação mensal, acumulada no ano, acum...
    URL                            http://sidra.ibge.gov.br/tabela/1419
    pesquisa              Índice Nacional de Preços ao Consumidor Amplo
    assunto                                           Índices de preços
    periodicidade     {'frequencia': 'mensal', 'inicio': 201201, 'fi...
    nivelTerritorial  {'Administrativo': ['N1', 'N6', 'N7'], 'Especi...
    variaveis         [{'id': 63, 'nome': 'IPCA - Variação mensal', ...
    classificacoes    [{'id': 315, 'nome': 'Geral, grupo, subgrupo, ...
    """
    url, _ = build_url(table)
    response = session.get(url)
    json = response.json()
    return json


def build_url(table: int) -> Tuple[str, None]:
    return f"https://servicodados.ibge.gov.br/api/v3/agregados/{table}/metadados", None
