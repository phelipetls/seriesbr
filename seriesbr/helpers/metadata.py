# Dictionaries of metadatas to query

ipea_metadata_list = [
    "SERNOME",
    "BASNOME",
    "TEMNOME",
    "UNINOME",
    "PERNOME",
    "FNTNOME",
    "SERCODIGO",
    "FNTSIGLA",
    "PAICODIGO",
    "SERCOMENTARIO",
]


def ipea_make_select_query(queried_fields):
    ordem = ["SERCODIGO", "PERNOME", "UNINOME", "SERNOME"]
    default = set({"SERCODIGO", "PERNOME", "UNINOME", "SERNOME"})
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
