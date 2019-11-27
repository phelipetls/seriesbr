def ipea_make_select_query(queried_fields):
    ordem = ["SERCODIGO", "PERNOME", "UNINOME", "SERNOME"]
    default = set({"SERCODIGO", "PERNOME", "UNINOME", "SERNOME"})
from pprint import pprint


    # to get the string
    # SERCODIGO,PERNOME,UNINOME,SERNOME,ANOTHERFILTER,ANOTHERFILTER
    # where ANOTHER must be something not alreay selected in default
    not_in_default = set(field for field in queried_fields) - default
    queried = ordem + list(not_in_default)
    return f"?$select={','.join(queried)}"


def ipea_make_filter_query(name, filters):
    # to get the string "&$filter=contains(SERNOME,'name')
    # and contains(ANOTHER,'value') and contains(ANOTHER,'value')"
    filter_query = f"&$filter=contains(SERNOME,'{name}')"
    if filters:
        filter_arguments = "and contains" + " and contains".join(
            f"({metadata},'{value}')"
            for metadata, value in filters.items()
        )
    return f"{filter_query}{filter_arguments if filters else ''}"
def print_suggestions():
    newline = "\n"
    metadatas = [
        print(metadado, descricao, end=newline)
        for metadado, descricao in ipea_metadata_list.items()
    ]
    suggestion_msg = f"These are not valid fields. Try one of these: {metadatas}"
    pprint(suggestion_msg)


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
