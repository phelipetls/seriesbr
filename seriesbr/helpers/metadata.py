# Dictionaries of metadatas to query

ipea_metadata_list = {
    "name": "SERNOME",
    "base": "BASNOME",
    "theme": "TEMNOME",
    "unit": "UNINOME",
    "period": "PERNOME",
    "source": "FNTNOME",
    "code": "SERCODIGO",
    "source_code": "FNTSIGLA",
    "region_code": "PAICODIGO",
    "description": "SERCOMENTARIO",
}


def ipea_make_select_query(selection):
    ordem = ["SERCODIGO", "PERNOME", "UNINOME", "SERNOME"]
    defaults = set({"SERCODIGO", "PERNOME", "UNINOME", "SERNOME"})
    # to get the string
    # SERCODIGO,PERNOME,UNINOME,SERNOME,ANOTHERFILTER,ANOTHERFILTER
    # where ANOTHER must be something not alreay selected in default
    additional = set([ipea_metadata_list[selected] for selected in selection]) - defaults
    queried = ordem + additional
    return f"?$select={','.join(queried)}"


def ipea_make_filter_query(name, filters):
    # to get the string "&$filter=contains(SERNOME,'name')
    # and contains(ANOTHER,'value') and contains(ANOTHER,'value')"
    filter_query = f"&$filter=contains(SERNOME,'{name}')"
    if filters:
        filter_arguments = "and contains" + " and contains".join(
            f"({ipea_metadata_list[metadata]},'{value}')"
            for metadata, value in filters.items()
        )
    return f"{filter_query}{filter_arguments if filters else ''}"
