def ipea_make_select_query(fields):
    # to get the string
    # SERCODIGO,PERNOME,UNINOME,SERNOME,ANOTHERFILTER,ANOTHERFILTER
    # where ANOTHER must be something not alreay selected by default
    defaults = ["SERCODIGO", "SERNOME", "PERNOME", "UNINOME"]
    selected = defaults + [field for field in fields if field not in defaults]
    return f"?$select={','.join(selected)}"


def ipea_make_filter_query(name, fields):
    # to get the string "&$filter=contains(SERNOME,'name')
    # and contains(ANOTHER,'value') and contains(ANOTHER,'value')"
    filter_query = f"&$filter=contains(SERNOME,'{name}')"
    if any([field not in ipea_metadata_list for field in fields]):
        raise ValueError(
            f"Can't search for {' or '.join(fields)}. Call ipea.list_fields() if you need help."
        )
    if fields:
        filter_arguments = " and contains" + " and contains".join(
            f"({metadata},'{value}')" for metadata, value in fields.items()
        )
        return f"{filter_query}{filter_arguments}"
    return f"{filter_query}"


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
