import pandas as pd

from seriesbr.helpers import metadata, request, utils, timeseries, lists, api


def get_series(
    code,
    variables=None,
    start=None,
    end=None,
    last_n=None,
    municipalities=None,
    states=None,
    macroregions=None,
    microregions=None,
    mesoregions=None,
    brazil=None,
    classifications=None,
):
    """
    Get an IBGE table

    Parameters
    ----------
    code : int
        Table code.

    variables : int or list of ints, optional
        Variables codes.

    start : int or str, optional
        Initial date, month or day first.

    end : int or str, optional
        Final date, month or day first.

    last_n : int or str, optional
        Return only last n observations.

    municipalities : str, int, bool a list, optional

    states : str, int, bool or a list, optional

    macroregions : str, int, bool or a list, optional

    microregions : str, int, bool or a list, optional

    mesoregions : str, int, bool or a list, optional

    classifications : dict, int, str or list, optional

    Returns
    -------
    pandas.DataFrame
        A DataFrame with series values and metadata.

    Examples
    --------
    >>> ibge.get_series(1419, start="11-2019", end="11-2019")
                Nível Territorial                              Variável   Geral, grupo, subgrupo, item e subitem   Valor
    Date
    2019-11-01            Brasil                 IPCA - Variação mensal   Índice geral                              0.51
    2019-11-01            Brasil       IPCA - Variação acumulada no ano   Índice geral                              3.12
    2019-11-01            Brasil  IPCA - Variação acumulada em 12 meses   Índice geral                              3.27
    2019-11-01            Brasil                     IPCA - Peso mensal   Índice geral                            100.00
    """
    baseurl = f"https://servicodados.ibge.gov.br/api/v3/agregados/{code}"

    frequency = get_frequency(code)
    dates = api.ibge_dates(start, end, last_n, frequency)
    variables = api.ibge_variables(variables)
    locations = api.ibge_locations(
        municipalities=municipalities,
        states=states,
        macroregions=macroregions,
        microregions=microregions,
        mesoregions=mesoregions,
        brazil=brazil,
    )
    classifications = api.ibge_classifications(classifications)

    url = f"{baseurl}{dates}{variables}?{classifications}{locations}&view=flat"
    return timeseries.ibge_json_to_df(url, frequency)


def get_frequency(table):
    """Get a table time frequency (periodicity)."""
    return list_periods(table).loc["frequencia", :].values


def build_url(table=""):
    """Return the url for a IBGE table."""
    return f"https://servicodados.ibge.gov.br/api/v3/agregados/{table}"


def get_metadata(table):
    """
    Get a IBGE table metadata.

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
    url = build_url(table) + "/metadados"
    return metadata.ibge_metadata_to_df(url)


def search(*search, **searches):
    """
    List all IBGE tables.

    Parameters
    ----------
    *search
        Strings to search for in a table name.

    **searches
        Strings to search in other field name,
        e.g. `pesquisa_nome`.

    Returns
    -------
    pandas.DataFrame

    Examples
    --------
    >>> ibge.search("Índice", "Preços", pesquisa_nome="Pesquisa").head()
            id                                               nome pesquisa_id                              pesquisa_nome
    2472  1399  Número de empresas comerciais, Unidades locais...          PB                 Pesquisa Anual de Comércio
    2957   379  Índice de Gini - recebimento médio mensal das ...          OF          Pesquisa de Orçamentos Familiares
    3101    50  Folha de pagamento nominal por classes de indú...          DG  Pesquisa Industrial Mensal - Dados Gerais
    3102    49  Folha de pagamento nominal por tipo de índice ...          DG  Pesquisa Industrial Mensal - Dados Gerais
    3103    52  Folha de pagamento nominal por trabalhador por...          DG  Pesquisa Industrial Mensal - Dados Gerais
    """
    url = build_url()
    json = request.get_json(url)

    df = utils.json_normalize(
        json, record_path="agregados", meta=["id", "nome"], meta_prefix="pesquisa_"
    )

    return utils.search_list(df, search, searches)


def list_variables(table, *search, **searches):
    """
    List all variables in a table.

    Returns
    -------
    pandas.DataFrame

    Examples
    --------
    >>> ibge.list_variables(1419)
         id                               variavel unidade
    0    63                 IPCA - Variação mensal       %
    1    69       IPCA - Variação acumulada no ano       %
    2  2265  IPCA - Variação acumulada em 12 meses       %
    3    66                     IPCA - Peso mensal       %
    """
    url = build_url(table)
    url += "/variaveis/all?localidades=BR"
    json = request.get_json(url)

    df = utils.json_normalize(json).iloc[:, :3]

    return utils.search_list(df, search, searches)


def list_locations(table):
    """
    List all locations available in a table.

    Examples
    --------
    >>> ibge.list_locations(1419)
      codes   locations
    0    N1      brazil
    1    N6        city
    2    N7  mesoregion
    """
    url = build_url(table) + "/metadados"
    metadata = request.get_json(url)

    codes = metadata["nivelTerritorial"]["Administrativo"]

    df = pd.DataFrame({"codes": codes})
    df["locations"] = df.codes.map(api.locations_codes_to_names)

    return df.loc[df.locations.notnull(), :]


def list_periods(table):
    """
    List a time series periodicity.

    Examples
    --------
    >>> ibge.list_periods(1419)
               valores
    frequencia  mensal
    inicio      201201
    fim         201911
    """
    metadata = get_metadata(table)
    periods = metadata.loc["periodicidade"][0]

    return pd.DataFrame(periods.values(), index=periods.keys(), columns=["valores"])


def list_classifications(table, *search, **searches):
    """
    List all classifications and categories in a table.

    Examples
    --------
    >>> ibge.list_classifications(1419).head()
         id                                     nome unidade  nivel classificacao_id                      classificacao_nome
    0  7169                             Índice geral    None     -1              315  Geral, grupo, subgrupo, item e subitem
    1  7170                  1.Alimentação e bebidas    None     -1              315  Geral, grupo, subgrupo, item e subitem
    2  7171              11.Alimentação no domicílio    None     -1              315  Geral, grupo, subgrupo, item e subitem
    3  7172  1101.Cereais, leguminosas e oleaginosas    None     -1              315  Geral, grupo, subgrupo, item e subitem
    4  7173                            1101002.Arroz    None     -1              315  Geral, grupo, subgrupo, item e subitem
    """
    classifications = get_metadata(table).loc["classificacoes"][0]

    df = utils.json_normalize(
        classifications, "categorias", meta=["id", "nome"], meta_prefix="classificacao_"
    )

    return utils.search_list(df, search, searches)


def list_states(*search, **searches):
    """
    List all states

    Examples
    --------
    >>> ibge.list_states().head()
       id sigla      nome  regiao_id regiao_sigla regiao_nome
    0  11    RO  Rondônia          1            N       Norte
    1  12    AC      Acre          1            N       Norte
    2  13    AM  Amazonas          1            N       Norte
    3  14    RR   Roraima          1            N       Norte
    4  15    PA      Pará          1            N       Norte
    """
    return lists.list_region("estados", search, searches)


def list_macroregions(*search, **searches):
    """
    List all macroregions

    Examples
    --------
    >>> ibge.list_macroregions()
       id sigla          nome
    0   1     N         Norte
    1   2    NE      Nordeste
    2   3    SE       Sudeste
    3   4     S           Sul
    4   5    CO  Centro-Oeste
    """
    return lists.list_region("regioes", search, searches)


def list_municipalities(*search, **searches):
    """
    List all municipalities

    Examples
    --------
    >>> ibge.list_cities(UF_nome="Rio de Janeiro").head()
               id                nome  microrregiao_id       microrregiao_nome  mesorregiao_id     mesorregiao_nome  UF_id UF_sigla         UF_nome  regiao_id regiao_sigla regiao_nome
    3175  3300100      Angra dos Reis            33013     Baía da Ilha Grande            3305       Sul Fluminense     33       RJ  Rio de Janeiro          3           SE     Sudeste
    3176  3300159             Aperibé            33002  Santo Antônio de Pádua            3301  Noroeste Fluminense     33       RJ  Rio de Janeiro          3           SE     Sudeste
    3177  3300209            Araruama            33010                   Lagos            3304             Baixadas     33       RJ  Rio de Janeiro          3           SE     Sudeste
    3178  3300225               Areal            33005               Três Rios            3303    Centro Fluminense     33       RJ  Rio de Janeiro          3           SE     Sudeste
    3179  3300233  Armação dos Búzios            33010                   Lagos            3304             Baixadas     33       RJ  Rio de Janeiro          3           SE     Sudeste
    """
    return lists.list_region("municipios", search, searches)


def list_microregions(*search, **searches):
    """
    List all microregions

    Examples
    --------
    >>> ibge.list_microregions("Rio", mesorregiao_nome="Rio")
            id                   nome  mesorregiao_id                 mesorregiao_nome  UF_id UF_sigla         UF_nome  regiao_id regiao_sigla regiao_nome
    348  33018         Rio de Janeiro            3306  Metropolitana do Rio de Janeiro     33       RJ  Rio de Janeiro          3           SE     Sudeste
    352  35004  São José do Rio Preto            3501            São José do Rio Preto     35       SP       São Paulo          3           SE     Sudeste
    """
    return lists.list_region("microrregioes", search, searches)


def list_mesoregions(*search, **searches):
    """
    List all mesoregions.

    Examples
    --------
    >>> ibge.list_mesoregions().head()
         id               nome  UF_id UF_sigla   UF_nome  regiao_id regiao_sigla regiao_nome
    0  1101    Madeira-Guaporé     11       RO  Rondônia          1            N       Norte
    1  1102  Leste Rondoniense     11       RO  Rondônia          1            N       Norte
    2  1201      Vale do Juruá     12       AC      Acre          1            N       Norte
    3  1202       Vale do Acre     12       AC      Acre          1            N       Norte
    4  1301   Norte Amazonense     13       AM  Amazonas          1            N       Norte
    """
    return lists.list_region("mesorregioes", search, searches)


# vi: nowrap
