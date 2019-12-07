from pandas import DataFrame
from .request import get_json
from .utils import clean_json, do_search

# IBGE


def list_regions(kind_of_region, search, where):
    url = f"https://servicodados.ibge.gov.br/api/v1/localidades/{kind_of_region}"
    json = get_json(url)
    df = clean_json(json)
    if search:
        return do_search(df, search, where)
    return df

# IPEA


def list_metadata(resource_path):
    baseurl = "http://www.ipeadata.gov.br/api/odata4/"
    url = f"{baseurl}{resource_path}"
    json = get_json(url)["value"]
    return DataFrame(json)


ipea_metadata_list = {
    "BASNOME": "Nome da base de dados da série.",
    "FNTNOME": "Nome completo da fonte da série, em português.",
    "FNTSIGLA": "Sigla ou nome abreviado da fonte da série, em português.",
    "FNTURL": "URL para o site da fonte da série.",
    "MULNOME": "Nome do fator multiplicador dos valores da série.",
    "PERNOME": "Nome da periodicidade, em português.",
    "SERATUALIZACAO": "Data da última carga de dados na série.",
    "SERCODIGO": "Código único de identificação da série.",
    "SERCOMENTARIO": "Comentários relativos a série, em português.",
    "SERNOME": "Nome da série, em português.",
    "UNINOME": "Nome da unidade dos valores da série.",
    "SERSTATUS": "Indica se uma série macroeconômica ainda é atualizada. Valores: ‘A’ (Ativa) para séries atualizadas ou ‘I’ (Inativa) para séries que não são atualizadas. As séries regionais ou sociais não possuem este metadado.",
    "TEMCODIGO": "Código de identificação do tema ao qual a série está associada.",
    "PAICODIGO": "Código de identificação país ou região (como América Latina, Zona do Euro, etc.) ao qual a série está associada. Deve ser levado em consideração apenas nas séries macroeconômicas (BASNOME = “Macroeconômico”); atualmente todas as séries regionais e sócias se referem ao Brasil, mesmo esta coluna PAICODIGO é nula ou vazia.",
    "SERNUMERICA": "Série numérica (1), série alfanumérica (0)",
}
