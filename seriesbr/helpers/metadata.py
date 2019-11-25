metadata_list = {
    "name": "SERNOME",
    "source": "FNTNOME",
    "source_code": "FNTSIGLA",
    "period": "SERNOME",
    "region_code": "PAICODIGO",
    "multiplo": "MULNOME",
    "base": "BASNOME",
    "comentario": "SERCOMENTARIO",
}


def make_select_query(queries):
    return "?$select=SERCODIGO," + ",".join(
        metadata_list[query] for query in queries if query in metadata_list
    )


def make_filter_query(queries):
    filter_query = "&$filter=contains("
    query_arguments = []
    for metadata, value in queries.items():
        if metadata in metadata_list:
            query_arguments.append(f"{metadata_list[metadata]},'{value}')")
    joined_arguments = query_arguments[0] + " and contains(".join([""] + query_arguments[1:])
    return f"{filter_query}{joined_arguments}"
